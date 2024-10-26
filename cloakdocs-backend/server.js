const express = require('express');
const multer = require('multer');
const { PDFDocument, rgb } = require('pdf-lib');
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const app = express();
const port = process.env.PORT || 5000;

// Setup file upload with Multer, restricting to image files (PNG, JPG, JPEG)
const upload = multer({
    dest: 'uploads/',
    fileFilter: (req, file, cb) => {
        const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        if (!allowedTypes.includes(file.mimetype)) {
            return cb(new Error('Only images are allowed'), false);
        }
        cb(null, true);
    },
});


// PDF Masking Endpoint
app.post('/mask-pdf', upload.single('file'), async (req, res) => {
    try {
        const pdfPath = req.file.path;
        const pdfBytes = fs.readFileSync(pdfPath);

        // Load the PDF with pdf-lib
        const pdfDoc = await PDFDocument.load(pdfBytes);
        const pages = pdfDoc.getPages();
        const firstPage = pages[0];

        // Draw a rectangle on the first page (this is a simple example mask)
        firstPage.drawRectangle({
            x: 50,
            y: 50,
            width: 200,
            height: 100,
            color: rgb(0, 0, 0),
        });

        // Save the modified PDF
        const maskedPdfBytes = await pdfDoc.save();
        fs.writeFileSync('uploads/masked-output.pdf', maskedPdfBytes);

        // Send the masked PDF back to the client
        res.download(path.resolve('uploads/masked-output.pdf'), 'masked-output.pdf');
    } catch (error) {
        console.error('Error processing PDF:', error);
        res.status(500).send('Error processing PDF');
    }
});

// Image Masking Endpoint
app.post('/mask-image', upload.single('file'), async (req, res) => {
    try {
        const imagePath = req.file.path;

        // Read the image using sharp and apply a simple black rectangle mask
        await sharp(imagePath)
            .composite([{ 
                input: Buffer.from(
                    '<svg><rect x="100" y="100" width="200" height="100" fill="black" /></svg>'
                ), 
                blend: 'over' 
            }])
            .toFile('uploads/masked-image.png');

        // Send the masked image back to the client
        res.download(path.resolve('uploads/masked-image.png'), 'masked-image.png');
    } catch (error) {
        console.error('Error processing image:', error);
        res.status(500).send('Error processing image');
    }
});


// Start the server
app.listen(port, () => console.log(`Server running on port ${port}`));
