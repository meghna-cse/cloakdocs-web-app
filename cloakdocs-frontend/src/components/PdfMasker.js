import React, { useEffect, useRef, useState } from 'react';
import { GlobalWorkerOptions, getDocument } from 'pdfjs-dist/build/pdf';

GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${GlobalWorkerOptions.version}/pdf.worker.min.js`;

const PdfMasker = ({ pdfSrc }) => {
    const canvasRef = useRef(null);
    const [context, setContext] = useState(null);

    useEffect(() => {
        const renderPdf = async () => {
            try {
                const pdf = await getDocument(pdfSrc).promise;
                const page = await pdf.getPage(1);
                const viewport = page.getViewport({ scale: 1.5 });

                const canvas = canvasRef.current;
                const context = canvas.getContext('2d');
                canvas.width = viewport.width;
                canvas.height = viewport.height;

                const renderContext = {
                    canvasContext: context,
                    viewport: viewport,
                };

                await page.render(renderContext).promise;
                setContext(context);

                // Create overlay canvas for drawing masks
                const overlayCanvas = document.createElement('canvas');
                overlayCanvas.width = canvas.width;
                overlayCanvas.height = canvas.height;
                overlayCanvas.style.position = 'absolute';
                overlayCanvas.style.top = '0';
                overlayCanvas.style.left = '0';
                overlayCanvas.style.pointerEvents = 'none'; // Prevent interference with underlying PDF
                canvas.parentNode.appendChild(overlayCanvas);
            } catch (error) {
                console.error("Error rendering PDF:", error);
            }
        };

        renderPdf();
    }, [pdfSrc]);

    const addMask = () => {
        if (context) {
            context.fillStyle = 'rgba(0, 0, 0, 0.5)';
            context.fillRect(100, 100, 150, 50); // Example mask coordinates
        }
    };

    return (
        <div style={{ position: 'relative' }}>
            <canvas ref={canvasRef} />
            <button onClick={addMask}>Add Mask</button>
        </div>
    );
};

export default PdfMasker;
