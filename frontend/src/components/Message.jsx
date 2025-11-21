import './Message.css'

const Message = ({ sender, text }) => {
    const isUser = sender === 'user'

    return (
        <div className={`message ${isUser ? 'user-message' : 'arcee-message'}`}>
            <div className='message-sender'>
                {isUser ? 'You' : 'Arcee'}
            </div>
            <div className='message-text'>
                {text}
            </div>
        </div>
    )
}

export default Message