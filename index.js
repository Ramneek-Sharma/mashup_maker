const express = require('express');
const bodyParser = require('body-parser');
const nodemailer = require('nodemailer');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const archiver = require('archiver');

const app = express();
const port = 3000;
const cors = require('cors');
app.use(cors());


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));


app.post('/process-audio', (req, res) => {
    const { singerName, email, numberOfAudios } = req.body;

    if (!singerName || !email || !numberOfAudios) {
        return res.status(400).json({ message: 'Missing required fields' });
    }

 
    exec(`python3 3.py --query "${singerName}" --max_results ${numberOfAudios}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).json({ message: 'Error processing audio files' });
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
        }


        const zipFilePath = `/Users/ramneeksharma/Desktop/mashup.zip`
        
        if (fs.existsSync(zipFilePath)) {
          
            let transporter = nodemailer.createTransport({
                service: 'gmail',
                auth: {
                    
                    user: 'sramneek2712@gmail.com',
                    pass: 'rqym lnqu ifpe awwe'     
                }
            });

            let mailOptions = {
                from: 'sramneek2712@gmail.com',    
                to: email,
                subject: 'Your Audio Mashup',
                text: `Hello ${email},\n\nPlease find the audio mashup attached.\n\nBest regards,\nAudio Team`,
                attachments: [
                    {
                        filename: 'mashup.zip',
                        path: zipFilePath
                    }
                ]
            };

            transporter.sendMail(mailOptions, (error, info) => {
                if (error) {
                    console.error(`Error sending email: ${error}`);
                    return res.status(500).json({ message: 'Error sending email' });
                }
                console.log('Email sent: ' + info.response);

                // Clean up
                fs.unlinkSync(zipFilePath);
                res.json({ message: 'Mashup processed and email sent' });
            });
        } else {
            console.error(`ZIP file not found: ${zipFilePath}`);
            return res.status(500).json({ message: 'ZIP file not found' });
        }
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});








// user: 'sramneek2712@gmail.com',
//                     pass: 'rqym lnqu ifpe awwe' 