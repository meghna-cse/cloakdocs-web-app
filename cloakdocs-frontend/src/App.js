import React, { useState } from 'react';
import FileUploader from './components/FileUploader';
import ImageMasker from './components/ImageMasker';
import PdfMasker from './components/PdfMasker';
import axios from 'axios';
import './App.css';

function App() {
    const [file, setFile] = useState(null);
    const [fileType, setFileType] = useState('');
    const [maskedFileUrl, setMaskedFileUrl] = useState('');

    const handleFileUpload = (uploadedFile) => {
        const fileExtension = uploadedFile.name.split('.').pop().toLowerCase();
        setFileType(fileExtension === 'pdf' ? 'pdf' : 'image');
        setFile(uploadedFile);
    };

    const handleMaskingSubmit = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(
                `http://localhost:5000/mask-${fileType}`,
                formData,
                {
                    headers: { 'Content-Type': 'multipart/form-data' },
                    responseType: 'blob', // Expect the server to send a blob (file)
                }
            );

            const blob = new Blob([response.data], {
                type: fileType === 'pdf' ? 'application/pdf' : 'image/png',
            });
            const url = window.URL.createObjectURL(blob);
            setMaskedFileUrl(url);
        } catch (error) {
            console.error('Error uploading or masking file:', error);
        }
    };

    return (
        <div className="App">
            <h1>CloakDocs - Mask Your Files</h1>
            <FileUploader onFileUpload={handleFileUpload} />
            {file && fileType === 'image' && <ImageMasker imageSrc={URL.createObjectURL(file)} />}
            {file && fileType === 'pdf' && <PdfMasker pdfSrc={URL.createObjectURL(file)} />}
            {file && (
                <button onClick={handleMaskingSubmit}>Submit for Masking</button>
            )}
            {maskedFileUrl && (
                <a href={maskedFileUrl} download={`masked-file.${fileType === 'pdf' ? 'pdf' : 'png'}`}>
                    Download Masked {fileType === 'pdf' ? 'PDF' : 'Image'}
                </a>
            )}
        </div>
    );
}

export default App;
