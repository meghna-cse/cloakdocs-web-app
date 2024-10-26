import React, { useRef, useEffect, useState } from 'react';
import { Canvas, Image, Rect } from 'fabric';

const ImageMasker = ({ imageSrc }) => {
    const canvasRef = useRef(null);
    const [canvas, setCanvas] = useState(null);

    useEffect(() => {
        const fabricCanvas = new Canvas(canvasRef.current);
        setCanvas(fabricCanvas);

        // Load the uploaded image onto the canvas
        Image.fromURL(imageSrc, (img) => {
            img.scaleToWidth(800);
            fabricCanvas.setWidth(800);
            fabricCanvas.setHeight(img.height * (800 / img.width));
            fabricCanvas.add(img);
            fabricCanvas.setActiveObject(img);
            img.selectable = false;
        });

        // Enable rectangle drawing mode
        const drawRect = () => {
            const rect = new Rect({
                left: 100,
                top: 100,
                width: 100,
                height: 50,
                fill: 'black',
                opacity: 0.5,
                selectable: true, // Allow the user to resize/move the mask
            });
            fabricCanvas.add(rect);
            fabricCanvas.setActiveObject(rect);
        };

        // Attach drawRect to a button or UI control
        document.getElementById('drawRectBtn').onclick = drawRect;

        return () => {
            fabricCanvas.dispose();
        };
    }, [imageSrc]);

    return (
        <div>
            <canvas ref={canvasRef} />
            <button id="drawRectBtn">Draw Mask</button>
        </div>
    );
};

export default ImageMasker;
