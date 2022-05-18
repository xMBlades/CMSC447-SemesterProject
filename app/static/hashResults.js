class Gauge extends HTMLElement {
    constructor() {
        super();

        const template = document.getElementById('gaugeTemplate');
        const templateContent = template.content;
        const shadowRoot = this.attachShadow({mode: "open"});
        const value = this.getAttribute('value');
        const label = this.getAttribute('label');
        const yellow = parseInt(this.getAttribute('yellow'));
        const red = parseInt(this.getAttribute('red'));
        const endAngle = -90 + ((value / 100) * 180);
        const dString = svgCircleArcPath(500, 500, 450, -90, endAngle);
        shadowRoot.appendChild(templateContent.cloneNode(true));

        const filled = shadowRoot.querySelector('.dataArc');
        const percentLabel = shadowRoot.querySelector('text.percentage');
        const textLabel = shadowRoot.querySelector('text.gaugeLabel');

        switch(true) {
            case value >= yellow && value < red:
                filled.classList.add('yellow');
                break;
            case value >= red:
                filled.classList.add('red');
                break;
        }

        percentLabel.textContent = `${value}%`;
        textLabel.textContent = label;
        filled.setAttribute('d', dString);
        
    }
}

function polarToCartesian(cx, cy, radius, angle) {
    const radians = (angle - 90) * Math.PI / 180.0;
    return [Math.round((cx + (radius * Math.cos(radians))) * 100) / 100, Math.round((cy + (radius * Math.sin(radians))) * 100) / 100];
}

function svgCircleArcPath(x, y, radius, startAngle, endAngle) {
    const startXY = polarToCartesian(x, y, radius, endAngle);
    const endXY = polarToCartesian(x, y, radius, startAngle);
    return `M ${startXY[0]} ${startXY[1]} A ${radius} ${radius} 0 0 0 ${endXY[0]} ${endXY[1]}`;
}

document.addEventListener('DOMContentLoaded', () => {
    customElements.define('percent-gauge', Gauge);
});