document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.container');
    const icons = Array.from(document.querySelectorAll('.icon-box'));
    const leftArrow = document.querySelector('.left-arrow');
    const rightArrow = document.querySelector('.right-arrow');
  
    function updateClasses() {
      icons.forEach(icon => {
        icon.classList.remove('left', 'center', 'right');
      });
  
      if (icons.length >= 3) {
        icons[0].classList.add('left');
        icons[1].classList.add('center');
        icons[2].classList.add('right');
      }
  
      icons.forEach(icon => {
        container.appendChild(icon);
      });
    }
  
    leftArrow.addEventListener('click', () => {
      const firstIcon = icons.shift();
      icons.push(firstIcon);
      updateClasses();
    });
  
    rightArrow.addEventListener('click', () => {
      const lastIcon = icons.pop();
      icons.unshift(lastIcon);
      updateClasses();
    });
  
    updateClasses();
});