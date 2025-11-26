/**
 * Logo Renderer - Creates SVG logos based on design parameters
 */

class LogoRenderer {
    constructor(design) {
        this.design = design;
        this.svgNS = "http://www.w3.org/2000/svg";
    }

    render() {
        const svg = document.createElementNS(this.svgNS, "svg");
        svg.setAttribute("viewBox", "0 0 300 300");
        svg.setAttribute("width", "100%");
        svg.setAttribute("height", "100%");

        // Background
        if (this.design.has_background) {
            const bg = this.createRect(0, 0, 300, 300, this.design.accent_color, 0.1);
            svg.appendChild(bg);
        }

        // Render based on style
        switch (this.design.style) {
            case 'minimal':
                this.renderMinimal(svg);
                break;
            case 'geometric':
                this.renderGeometric(svg);
                break;
            case 'circular':
                this.renderCircular(svg);
                break;
            case 'badge':
                this.renderBadge(svg);
                break;
            case 'wordmark':
                this.renderWordmark(svg);
                break;
            case 'lettermark':
                this.renderLettermark(svg);
                break;
            case 'abstract':
                this.renderAbstract(svg);
                break;
            case 'emblem':
                this.renderEmblem(svg);
                break;
            case 'combination':
                this.renderCombination(svg);
                break;
            default:
                this.renderMinimal(svg);
        }

        return svg;
    }

    createRect(x, y, width, height, fill, opacity = 1) {
        const rect = document.createElementNS(this.svgNS, "rect");
        rect.setAttribute("x", x);
        rect.setAttribute("y", y);
        rect.setAttribute("width", width);
        rect.setAttribute("height", height);
        rect.setAttribute("fill", fill);
        rect.setAttribute("opacity", opacity);
        return rect;
    }

    createCircle(cx, cy, r, fill, opacity = 1) {
        const circle = document.createElementNS(this.svgNS, "circle");
        circle.setAttribute("cx", cx);
        circle.setAttribute("cy", cy);
        circle.setAttribute("r", r);
        circle.setAttribute("fill", fill);
        circle.setAttribute("opacity", opacity);
        return circle;
    }

    createText(x, y, text, fontSize, fill, fontWeight = "bold", textAnchor = "middle") {
        const textEl = document.createElementNS(this.svgNS, "text");
        textEl.setAttribute("x", x);
        textEl.setAttribute("y", y);
        textEl.setAttribute("font-size", fontSize);
        textEl.setAttribute("fill", fill);
        textEl.setAttribute("font-weight", fontWeight);
        textEl.setAttribute("text-anchor", textAnchor);
        textEl.setAttribute("dominant-baseline", "middle");
        textEl.setAttribute("font-family", "Arial, sans-serif");
        textEl.textContent = text;
        return textEl;
    }

    createPath(d, fill, opacity = 1) {
        const path = document.createElementNS(this.svgNS, "path");
        path.setAttribute("d", d);
        path.setAttribute("fill", fill);
        path.setAttribute("opacity", opacity);
        return path;
    }

    renderMinimal(svg) {
        // Simple icon with text
        const icon = this.createShape(150, 120, 50, this.design.primary_color);
        svg.appendChild(icon);

        const text = this.createText(150, 200, this.design.company_name, 24, this.design.primary_color);
        svg.appendChild(text);
    }

    renderGeometric(svg) {
        // Multiple geometric shapes
        const shape1 = this.createRect(100, 80, 60, 60, this.design.primary_color);
        shape1.setAttribute("transform", `rotate(45 130 110)`);
        svg.appendChild(shape1);

        const shape2 = this.createRect(140, 80, 60, 60, this.design.secondary_color);
        shape2.setAttribute("transform", `rotate(45 170 110)`);
        svg.appendChild(shape2);

        const text = this.createText(150, 200, this.design.company_name, 22, this.design.primary_color);
        svg.appendChild(text);
    }

    renderCircular(svg) {
        // Concentric circles
        const circle1 = this.createCircle(150, 150, 80, this.design.primary_color);
        svg.appendChild(circle1);

        const circle2 = this.createCircle(150, 150, 60, this.design.secondary_color);
        svg.appendChild(circle2);

        const initials = this.createText(150, 150, this.design.initials, 48, "white");
        svg.appendChild(initials);

        const text = this.createText(150, 250, this.design.company_name, 20, this.design.primary_color);
        svg.appendChild(text);
    }

    renderBadge(svg) {
        // Badge style with border
        const outerCircle = this.createCircle(150, 150, 90, this.design.primary_color);
        svg.appendChild(outerCircle);

        const innerCircle = this.createCircle(150, 150, 75, "white");
        svg.appendChild(innerCircle);

        const centerCircle = this.createCircle(150, 150, 60, this.design.secondary_color);
        svg.appendChild(centerCircle);

        const initials = this.createText(150, 150, this.design.initials, 42, "white");
        svg.appendChild(initials);

        const text = this.createText(150, 260, this.design.company_name, 18, this.design.primary_color);
        svg.appendChild(text);
    }

    renderWordmark(svg) {
        // Text-only logo
        const mainText = this.createText(150, 140, this.design.company_name, 36, this.design.primary_color, "900");
        svg.appendChild(mainText);

        // Decorative underline
        const line = this.createRect(75, 160, 150, 4, this.design.secondary_color);
        line.setAttribute("rx", 2);
        svg.appendChild(line);
    }

    renderLettermark(svg) {
        // Large initials
        const bg = this.createRect(75, 75, 150, 150, this.design.primary_color);
        bg.setAttribute("rx", this.design.border_radius);
        svg.appendChild(bg);

        const initials = this.createText(150, 150, this.design.initials, 72, "white", "900");
        svg.appendChild(initials);

        const text = this.createText(150, 250, this.design.company_name, 18, this.design.primary_color);
        svg.appendChild(text);
    }

    renderAbstract(svg) {
        // Abstract flowing shapes
        const path1 = this.createPath(
            `M 80,150 Q 100,80 150,100 T 220,150 Q 200,180 150,170 T 80,150`,
            this.design.primary_color
        );
        svg.appendChild(path1);

        const path2 = this.createPath(
            `M 90,160 Q 110,100 150,115 T 210,160`,
            this.design.secondary_color,
            0.7
        );
        svg.appendChild(path2);

        const text = this.createText(150, 230, this.design.company_name, 22, this.design.primary_color);
        svg.appendChild(text);
    }

    renderEmblem(svg) {
        // Shield-like emblem
        const shield = this.createPath(
            `M 150,60 L 220,90 L 220,170 Q 220,220 150,240 Q 80,220 80,170 L 80,90 Z`,
            this.design.primary_color
        );
        svg.appendChild(shield);

        const innerShield = this.createPath(
            `M 150,80 L 200,100 L 200,165 Q 200,205 150,220 Q 100,205 100,165 L 100,100 Z`,
            this.design.secondary_color
        );
        svg.appendChild(innerShield);

        const initials = this.createText(150, 150, this.design.initials, 48, "white", "900");
        svg.appendChild(initials);

        const text = this.createText(150, 270, this.design.company_name, 18, this.design.primary_color);
        svg.appendChild(text);
    }

    renderCombination(svg) {
        // Icon + text combination
        const iconBg = this.createCircle(150, 110, 45, this.design.primary_color);
        svg.appendChild(iconBg);

        const icon = this.createShape(150, 110, 30, "white");
        svg.appendChild(icon);

        const text = this.createText(150, 190, this.design.company_name, 28, this.design.primary_color, "bold");
        svg.appendChild(text);

        const tagline = this.createText(150, 215, "Quality & Innovation", 12, this.design.secondary_color, "normal");
        svg.appendChild(tagline);
    }

    createShape(cx, cy, size, fill) {
        // Create different shapes based on design.shape
        switch (this.design.shape) {
            case 'circle':
                return this.createCircle(cx, cy, size, fill);
            case 'square':
                const rect = this.createRect(cx - size, cy - size, size * 2, size * 2, fill);
                rect.setAttribute("rx", 5);
                return rect;
            case 'triangle':
                return this.createPath(
                    `M ${cx},${cy - size} L ${cx + size},${cy + size} L ${cx - size},${cy + size} Z`,
                    fill
                );
            case 'hexagon':
                const hex = size * 0.866;
                return this.createPath(
                    `M ${cx},${cy - size} L ${cx + hex},${cy - size/2} L ${cx + hex},${cy + size/2} L ${cx},${cy + size} L ${cx - hex},${cy + size/2} L ${cx - hex},${cy - size/2} Z`,
                    fill
                );
            case 'diamond':
                return this.createPath(
                    `M ${cx},${cy - size} L ${cx + size},${cy} L ${cx},${cy + size} L ${cx - size},${cy} Z`,
                    fill
                );
            case 'star':
                const star = this.createStar(cx, cy, 5, size, size * 0.5);
                star.setAttribute("fill", fill);
                return star;
            default:
                return this.createCircle(cx, cy, size, fill);
        }
    }

    createStar(cx, cy, points, outerRadius, innerRadius) {
        let path = "";
        const angle = Math.PI / points;
        
        for (let i = 0; i < 2 * points; i++) {
            const r = (i % 2 === 0) ? outerRadius : innerRadius;
            const currAngle = i * angle - Math.PI / 2;
            const x = cx + r * Math.cos(currAngle);
            const y = cy + r * Math.sin(currAngle);
            path += (i === 0 ? "M" : "L") + ` ${x},${y}`;
        }
        path += " Z";
        
        return this.createPath(path, "");
    }
}
