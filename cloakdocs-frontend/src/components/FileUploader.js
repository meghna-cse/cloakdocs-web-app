import React from 'react';
import { useDropzone } from 'react-dropzone';
import './FileUploader.css'; // Add custom styles for the drag-and-drop zone

const FileUploader = ({ onFileUpload }) => {
    const { getRootProps, getInputProps } = useDropzone({
        onDrop: (acceptedFiles) => onFileUpload(acceptedFiles[0]),
        accept: '.jpg, .jpeg, .png, .pdf', // Allow images and PDFs
        multiple: false, // Accept only one file at a time
    });

    return (
        <div {...getRootProps({ className: 'dropzone' })}>
            <input {...getInputProps()} />
            <p>Drag & drop a file here, or click to select a file</p>
        </div>
    );
};

export default FileUploader;
