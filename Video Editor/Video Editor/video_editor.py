from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import ffmpeg
import os
import tempfile
from werkzeug.utils import secure_filename
import subprocess
import time
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov', 'mkv'}

def get_video_info(file_path):
    try:
        probe = ffmpeg.probe(file_path)
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        return {
            'width': int(video_info['width']),
            'height': int(video_info['height']),
            'codec': video_info['codec_name']
        }
    except Exception as e:
        raise Exception(f"Error getting video info: {str(e)}")

def safe_remove_file(file_path, max_attempts=3):
    """Safely remove a file with retries"""
    for attempt in range(max_attempts):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except PermissionError:
            if attempt < max_attempts - 1:
                time.sleep(1)  # Wait before retrying
            continue
    return False

@app.route('/resize', methods=['POST'])
def resize_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    video = request.files['video']
    if video.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not video.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        return jsonify({'error': 'Invalid file type. Supported formats: MP4, AVI, MOV, MKV'}), 400
    
    try:
        width = int(request.form.get('width', 0))
        height = int(request.form.get('height', 0))
        
        if width <= 0 or height <= 0:
            return jsonify({'error': 'Invalid dimensions'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid dimension values'}), 400
    
    temp_dir = None
    try:
        # Create a temporary directory for processing
        temp_dir = tempfile.mkdtemp()
        
        # Save the uploaded video
        input_path = os.path.join(temp_dir, 'input.mp4')
        video.save(input_path)
        
        # Get video info
        probe = ffmpeg.probe(input_path)
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        original_width = int(video_info['width'])
        original_height = int(video_info['height'])
        
        # Calculate new dimensions maintaining aspect ratio
        aspect_ratio = original_width / original_height
        if width / height > aspect_ratio:
            new_width = int(height * aspect_ratio)
            new_height = height
        else:
            new_width = width
            new_height = int(width / aspect_ratio)
        
        # Output path
        output_path = os.path.join(temp_dir, 'output.mp4')
        
        # Resize video using FFmpeg with improved settings
        input_stream = ffmpeg.input(input_path)
        
        # Apply video scaling
        video_stream = input_stream.video.filter('scale', new_width, new_height, force_original_aspect_ratio='decrease')
        
        # Keep audio stream as is
        audio_stream = input_stream.audio
        
        # Combine video and audio streams
        stream = ffmpeg.output(
            video_stream,
            audio_stream,
            output_path,
            vcodec='libx264',
            acodec='aac',
            video_bitrate='2500k',
            audio_bitrate='192k',
            preset='medium',
            movflags='+faststart',
            pix_fmt='yuv420p',
            ac=2,  # Set to stereo
            ar='44100'  # Set sample rate to 44.1kHz
        )
        
        ffmpeg.run(stream, overwrite_output=True)
        
        # Read the file into memory
        with open(output_path, 'rb') as f:
            file_data = f.read()
        
        # Clean up the temporary files
        safe_remove_file(input_path)
        safe_remove_file(output_path)
        
        # Send the resized video from memory
        return send_file(
            io.BytesIO(file_data),
            mimetype='video/mp4',
            as_attachment=True,
            download_name='resized_video.mp4'
        )
            
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        return jsonify({'error': 'Error processing video'}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass

@app.route('/trim', methods=['POST'])
def trim_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    video = request.files['video']
    if video.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not video.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        return jsonify({'error': 'Invalid file type. Supported formats: MP4, AVI, MOV, MKV'}), 400
    
    try:
        start_time = float(request.form.get('start_time', 0))
        end_time = float(request.form.get('end_time', 0))
        
        if start_time >= end_time or start_time < 0:
            return jsonify({'error': 'Invalid time range'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid time values'}), 400
    
    temp_dir = None
    try:
        # Create a temporary directory for processing
        temp_dir = tempfile.mkdtemp()
        
        # Save the uploaded video
        input_path = os.path.join(temp_dir, 'input.mp4')
        video.save(input_path)
        
        # Output path
        output_path = os.path.join(temp_dir, 'output.mp4')
        
        # Trim video using FFmpeg
        stream = ffmpeg.input(input_path, ss=start_time, t=end_time-start_time)
        stream = ffmpeg.output(
            stream,
            output_path,
            acodec='copy',  # Copy audio without re-encoding
            vcodec='copy',  # Copy video without re-encoding
            movflags='+faststart'  # Enable fast start for web playback
        )
        
        ffmpeg.run(stream, overwrite_output=True)
        
        # Read the file into memory
        with open(output_path, 'rb') as f:
            file_data = f.read()
        
        # Clean up the temporary files
        safe_remove_file(input_path)
        safe_remove_file(output_path)
        
        # Send the trimmed video from memory
        return send_file(
            io.BytesIO(file_data),
            mimetype='video/mp4',
            as_attachment=True,
            download_name='trimmed_video.mp4'
        )
            
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        return jsonify({'error': 'Error processing video'}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass

@app.route('/merge', methods=['POST'])
def merge_videos():
    if 'videos' not in request.files:
        return jsonify({'error': 'No video files provided'}), 400
    
    videos = request.files.getlist('videos')
    if not videos or videos[0].filename == '':
        return jsonify({'error': 'No selected files'}), 400
    
    temp_dir = None
    try:
        # Create a temporary directory for processing
        temp_dir = tempfile.mkdtemp()
        
        # Save all uploaded videos
        video_paths = []
        for i, video in enumerate(videos):
            if not video.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                raise ValueError(f'Invalid file type for video {i+1}. Supported formats: MP4, AVI, MOV, MKV')
            
            video_path = os.path.join(temp_dir, f'input_{i}.mp4')
            video.save(video_path)
            video_paths.append(video_path)
        
        # Get video info from first video
        first_video_info = get_video_info(video_paths[0])
        
        # Convert all videos to match first video's format and fix timestamps
        converted_paths = []
        for i, video_path in enumerate(video_paths):
            converted_path = os.path.join(temp_dir, f'converted_{i}.mp4')
            stream = ffmpeg.input(video_path)
            stream = ffmpeg.output(
                stream,
                converted_path,
                vcodec='libx264',
                acodec='aac',
                video_bitrate='2500k',
                audio_bitrate='192k',
                preset='medium',
                movflags='+faststart',
                pix_fmt='yuv420p',
                vsync='vfr',  # Variable frame rate
                max_interleave_delta='0',  # Fix timestamp issues
                ac=2,  # Set to stereo
                ar='44100'  # Set sample rate to 44.1kHz
            )
            ffmpeg.run(stream, overwrite_output=True)
            converted_paths.append(converted_path)
        
        # Create concat file with absolute paths
        concat_file = os.path.join(temp_dir, 'concat.txt')
        with open(concat_file, 'w') as f:
            for path in converted_paths:
                f.write(f"file '{os.path.abspath(path)}'\n")
        
        # Output path
        output_path = os.path.join(temp_dir, 'output.mp4')
        
        # Merge videos using FFmpeg with improved settings
        stream = ffmpeg.input(concat_file, format='concat', safe=0)
        stream = ffmpeg.output(
            stream,
            output_path,
            vcodec='libx264',
            acodec='aac',
            video_bitrate='2500k',
            audio_bitrate='192k',
            preset='medium',
            movflags='+faststart',
            pix_fmt='yuv420p',
            vsync='vfr',  # Variable frame rate
            max_interleave_delta='0',  # Fix timestamp issues
            ac=2,  # Set to stereo
            ar='44100'  # Set sample rate to 44.1kHz
        )
        
        ffmpeg.run(stream, overwrite_output=True)
        
        # Read the file into memory
        with open(output_path, 'rb') as f:
            file_data = f.read()
        
        # Clean up the temporary files
        for path in video_paths + converted_paths + [concat_file, output_path]:
            safe_remove_file(path)
        
        # Send the merged video from memory
        return send_file(
            io.BytesIO(file_data),
            mimetype='video/mp4',
            as_attachment=True,
            download_name='merged_video.mp4'
        )
            
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        return jsonify({'error': 'Error processing videos'}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass

@app.route('/remove_audio', methods=['POST'])
def remove_audio():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    video = request.files['video']
    if video.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not video.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        return jsonify({'error': 'Invalid file type. Supported formats: MP4, AVI, MOV, MKV'}), 400
    
    temp_dir = None
    try:
        # Create a temporary directory for processing
        temp_dir = tempfile.mkdtemp()
        
        # Save the uploaded video
        input_path = os.path.join(temp_dir, 'input.mp4')
        video.save(input_path)
        
        # Output path
        output_path = os.path.join(temp_dir, 'output.mp4')
        
        # Remove audio using FFmpeg
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(
            stream,
            output_path,
            an=None,  # Remove audio
            vcodec='copy',  # Copy video without re-encoding
            movflags='+faststart'  # Enable fast start for web playback
        )
        
        ffmpeg.run(stream, overwrite_output=True)
        
        # Read the file into memory
        with open(output_path, 'rb') as f:
            file_data = f.read()
        
        # Clean up the temporary files
        safe_remove_file(input_path)
        safe_remove_file(output_path)
        
        # Send the video without audio from memory
        return send_file(
            io.BytesIO(file_data),
            mimetype='video/mp4',
            as_attachment=True,
            download_name='video_without_audio.mp4'
        )
            
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        return jsonify({'error': 'Error processing video'}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass

@app.route('/extract_audio', methods=['POST'])
def extract_audio():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    video = request.files['video']
    if video.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not video.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        return jsonify({'error': 'Invalid file type. Supported formats: MP4, AVI, MOV, MKV'}), 400
    
    temp_dir = None
    try:
        # Create a temporary directory for processing
        temp_dir = tempfile.mkdtemp()
        
        # Save the uploaded video
        input_path = os.path.join(temp_dir, 'input.mp4')
        video.save(input_path)
        
        # Output path for audio
        output_path = os.path.join(temp_dir, 'output.mp3')
        
        # Extract audio using FFmpeg
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(
            stream,
            output_path,
            acodec='libmp3lame',  # Use MP3 codec
            audio_bitrate='192k',  # Set bitrate for good quality
            ac=2,  # Set to stereo
            ar='44100'  # Set sample rate to 44.1kHz
        )
        ffmpeg.run(stream, overwrite_output=True)
        
        # Read the file into memory
        with open(output_path, 'rb') as f:
            file_data = f.read()
        
        # Clean up the temporary files
        safe_remove_file(input_path)
        safe_remove_file(output_path)
        
        # Send the extracted audio from memory
        return send_file(
            io.BytesIO(file_data),
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='extracted_audio.mp3'
        )
            
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        return jsonify({'error': 'Error processing video'}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass

if __name__ == '__main__':
    app.run(debug=True) 