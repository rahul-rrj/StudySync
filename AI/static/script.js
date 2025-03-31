document.getElementById("inputText").addEventListener("input", function () {
    let text = this.value.trim();
    let wordCount = text.split(/\s+/).filter(word => word.length > 0).length;
    
    document.getElementById("wordCount").innerText = wordCount + " / 300 words";
    
    if (wordCount > 300) {
        this.value = text.split(/\s+/).slice(0, 300).join(" "); // Trim extra words
        document.getElementById("wordCount").innerText = "300 / 300 words (Limit Reached)";
    }
});

async function generateAI() {
    let text = document.getElementById("inputText").value.trim();
    if (!text) {
        document.getElementById("output").innerText = "Please enter some text!";
        return;
    }

    document.getElementById("output").innerText = "Processing AI response...";
    
    try {
        let response = await fetch("/ai_writer", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });

        let result = await response.json();
        console.log("AI Response:", result);

        document.getElementById("output").innerText = result.generated_text || "No response!";
    } catch (error) {
        console.error("Error in AI Writer:", error);
        document.getElementById("output").innerText = "Error generating AI response!";
    }
}
async function checkGrammar() {
    let text = document.getElementById("inputText").value;
    let response = await fetch("/grammar_check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
    });

    let result = await response.json();
    
    if (result.corrected_text) {
        document.getElementById("output").innerHTML = 
            `<strong>Corrected Sentence:</strong> ${result.corrected_text}`;
    } else {
        document.getElementById("output").innerText = "No changes needed!";
    }
}


async function takeNotes() {
    let text = document.getElementById("inputText").value;
    let response = await fetch("/notes_taker", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
    });
    let result = await response.json();
    document.getElementById("output").innerText = result.notes || "Error taking notes!";
}

