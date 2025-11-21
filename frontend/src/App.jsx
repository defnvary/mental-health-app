import { useState } from 'react'
import axios from 'axios'
import Message from './components/Message'
import CrisisAlert from './components/CrisisAlert'
import './App.css'

const App = () => {
  // State Management
  const [messages, setMessages] = useState([])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  // API endpoint
  const API_URL = 'http://localhost:5000/chat'

  // send message function
  const sendMessage = async () => {
    if (!inputText.trim()) return

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      text: inputText,
      isCrisis: false
    }

    // add user message to chat
    setMessages(prev => [...prev, userMessage])
    setInputText('')
    setIsLoading(true)

    try {
      // call backend api
      const response = await axios.post(API_URL, {
        message: inputText
      })

      const data = response.data

      // create arcee's response message
      const arceeMessage = {
        id: Date.now() + 1,
        sender: 'arcee',
        text: data.response,
        isCrisis: data.is_crisis,
        crisisResources: data.crisis_resources || null
      }

      // add arcee's message to chat
      setMessages(prev => [...prev, arceeMessage])
    } catch (error) {
      console.log("Error sending message: ", error)

      // show error message
      const errorMessage = {
        id: Date.now() + 1,
        sender: 'arcee',
        text: 'Sorry, I encountered an error, please try again.',
        isCrisis: false
      }

      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }


  return (
    <div className='app'>
      <header className='header'>
        <h1>Arcee</h1>
        <p className='subtitle'>Student Mental Health Companion</p>
      </header>

      <main className='chat-container'>
        <div className='messages'>
          {/* Messages will go here */}
          {messages.length === 0 ? (
            <div className='welcome-message'>
              <p>Hi! I'm Arcee</p>
              <p>How are you feeling today?</p>
            </div>
          ) : (
            messages.map((msg) => (
              <div key={msg.id}>
                {msg.isCrisis && msg.crisisResources && (
                  <CrisisAlert resources={msg.crisisResources} />
                )}
                <Message sender={msg.sender} text={msg.text} />
              </div>
            ))
          )}

          {isLoading && (
            <div className='typing-indicator'>
              <span>Arcee is typing</span>
              <span className='dots'>...</span>
            </div>
          )}
        </div>
      </main>

      <footer className="input-area">
        <div className='input-area-container'>
          {/* Input will go here */}
          <textarea value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Share what's on your mind..."
            rows='3'
            disabled={isLoading}
          />

          <button
            // onClick={() => console.log('Send clicked')}
            onClick={sendMessage}
            disabled={!inputText.trim() || isLoading}
          >Send</button>
        </div>
      </footer>
    </div>
  )
}

export default App