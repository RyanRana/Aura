import React, { useState, useEffect, useRef } from 'react';
import { Box, Container, Typography, TextField, IconButton, Paper, CircularProgress, Button, Stack, Card, CardContent, CardActions } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import API_BASE_URL from '../config';

function Chatbox() {
  const [messages, setMessages] = useState([
    { type: 'text', sender: 'aura', text: "Hello! I'm Aura... What would you like to explore today?" }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Set page title
  useEffect(() => {
    document.title = 'Aura - Chatbox';
  }, []);

  const scrollToBottom = () => { chatEndRef.current?.scrollIntoView({ behavior: "smooth" }); };
  useEffect(() => { scrollToBottom(); }, [messages, isLoading]);

  const handleSend = async () => {
    if (input.trim() === '' || isLoading) return;
    const userMessage = { type: 'text', sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/chat`, { message: input, history: messages });
      const auraMessage = { type: 'text', sender: 'aura', text: response.data.response };
      setMessages(prev => [...prev, auraMessage]);
    } catch (error) {
      console.error("API Error:", error);
      const errorMessage = { type: 'text', sender: 'aura', text: "Sorry, I'm having trouble connecting." };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const onDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setMessages(prev => [...prev, { type: 'text', sender: 'user', text: `Attaching file: ${file.name}...` }]);
    setIsLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Call the first endpoint to get the plan
      const response = await axios.post(`${API_BASE_URL}/api/analyze-csv`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      // Add a special "plan" message to the chat
      setMessages(prev => [...prev, { type: 'plan', sender: 'aura', plan: response.data }]);
    } catch (error) {
      console.error("File analysis error:", error);
      const errorText = error.response?.data?.error || "Failed to analyze the file.";
      setMessages(prev => [...prev, { type: 'text', sender: 'aura', text: errorText }]);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleConfirmUpload = async (plan) => {
    // Disable the buttons after one is clicked
    setMessages(messages.map(m => m.plan === plan ? { ...m, plan: { ...plan, confirmed: true } } : m));
    setIsLoading(true);

    try {
        // Call the second endpoint to execute the upload
        const response = await axios.post(`${API_BASE_URL}/api/execute-upload`, plan);
        setMessages(prev => [...prev, { type: 'text', sender: 'aura', text: response.data.message }]);
    } catch (error) {
        console.error("Upload execution error:", error);
        const errorText = error.response?.data?.error || "Failed to upload the data.";
        setMessages(prev => [...prev, { type: 'text', sender: 'aura', text: errorText }]);
    } finally {
        setIsLoading(false);
    }
  };

  const { getRootProps, getInputProps, open } = useDropzone({
    onDrop, noClick: true, noKeyboard: true, accept: { 'text/csv': ['.csv'] },
  });

  const exampleQuestions = ['BOGO Avocado Profitability', 'Banana Stockout Analysis', 'Avocado Loss Investigation'];

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" align="center" gutterBottom sx={{ fontWeight: 'bold' }}>AURA</Typography>
      <Typography variant="subtitle1" color="text.secondary" align="center" sx={{ mb: 4 }}>
        Your Retail Intelligence Partner. Ask strategic questions for data-driven Insights.
      </Typography>

      <Paper {...getRootProps()} elevation={3} sx={{ height: '60vh', display: 'flex', flexDirection: 'column', backgroundColor: '#1e1e1e', outline: 'none' }}>
        <input {...getInputProps()} />
        <Box sx={{ flexGrow: 1, overflowY: 'auto', p: 2 }}>
          {messages.map((msg, index) => {
            if (msg.type === 'plan') {
              return <UploadPlanCard key={index} plan={msg.plan} onConfirm={handleConfirmUpload} />;
            }
            return <MessageBubble key={index} sender={msg.sender} text={msg.text} />;
          })}
          {isLoading && <TypingIndicator />}
          <div ref={chatEndRef} />
        </Box>

        <Stack direction="row" spacing={1} sx={{ p: 2, borderTop: '1px solid #333' }}>
            <Typography variant="caption" sx={{mr: 1, alignSelf: 'center', color: 'text.secondary'}}>Examples:</Typography>
            {exampleQuestions.map(q => (
                <Button key={q} size="small" variant="outlined" sx={{borderRadius: '16px', color: 'text.secondary', borderColor: '#555'}} onClick={() => setInput(q)}>{q}</Button>
            ))}
        </Stack>
        
        <Box sx={{ p: 2, borderTop: '1px solid #333' }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <IconButton onClick={open} sx={{ mr: 1, color: 'text.secondary' }}><AttachFileIcon /></IconButton>
            <TextField fullWidth variant="standard" placeholder="Ask Aura your question..." value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              InputProps={{ disableUnderline: true }}
              disabled={isLoading}
            />
            <IconButton color="primary" onClick={handleSend} disabled={isLoading || input.trim() === ''}><SendIcon /></IconButton>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
}

// --- Child Components ---

const MessageBubble = ({ sender, text }) => (
  <Box sx={{ display: 'flex', justifyContent: sender === 'user' ? 'flex-end' : 'flex-start', mb: 2 }}>
    <Paper sx={{ p: 1.5, maxWidth: '70%', backgroundColor: sender === 'user' ? 'primary.main' : '#333', borderRadius: sender === 'user' ? '20px 20px 5px 20px' : '20px 20px 20px 5px' }}>
      <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>{text}</Typography>
    </Paper>
  </Box>
);

const TypingIndicator = () => (
  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
    <CircularProgress size={20} sx={{ mr: 1.5 }} />
    <Box>
      <Typography variant="body1" component="span" color="text.secondary">Aura is working...</Typography>
    </Box>
  </Box>
);

const UploadPlanCard = ({ plan, onConfirm }) => (
  <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 2 }}>
    <Card sx={{ maxWidth: '70%', backgroundColor: '#333' }}>
      <CardContent>
        <Typography gutterBottom variant="h6" component="div">Upload Plan</Typography>
        <Typography variant="body2">
          I've analyzed the CSV. I suggest uploading this data to the <strong>{plan.suggested_table}</strong> table.
        </Typography>
        <Typography variant="body2" sx={{ mt: 1 }}>Here is the proposed column mapping:</Typography>
        <Paper variant="outlined" sx={{ p: 1, mt: 1, maxHeight: 100, overflowY: 'auto', fontSize: '0.8rem', backgroundColor: '#222' }}>
          {Object.entries(plan.column_mapping).map(([csvCol, dbCol]) => (
            <div key={csvCol}>{`'${csvCol}'  →  '${dbCol || 'NULL'}'`}</div>
          ))}
        </Paper>
      </CardContent>
      <CardActions sx={{ justifyContent: 'flex-end' }}>
        <Button size="small" disabled={plan.confirmed}>Cancel</Button>
        <Button size="small" onClick={() => onConfirm(plan)} disabled={plan.confirmed}>Confirm</Button>
      </CardActions>
    </Card>
  </Box>
);

export default Chatbox;