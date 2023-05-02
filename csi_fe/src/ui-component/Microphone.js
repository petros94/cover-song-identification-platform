import React from "react";
import { ReactMediaRecorder } from "react-media-recorder";

const Microphone = () => (
    <>
        <ReactMediaRecorder
            audio
            onStop={(blobUrl, blob) => { console.log(blob) }}
            render={({ status, startRecording, stopRecording }) => (
                <div>
                    <p>{status}</p>
                    <button onClick={startRecording}>Start Recording</button>
                    <button onClick={stopRecording}>Stop Recording</button>
                </div>
            )}
        />
    </>
);

export default Microphone;