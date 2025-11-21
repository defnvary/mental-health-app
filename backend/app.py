import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime

# load env variables
load_dotenv()

# initialize app
app = Flask(__name__)

# enable cors for communicating with frontend (instead of just CORS(app))
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# system_instructions
SYSTEM_INSTRUCTIONS = """
You are Arcee, a mental health support companion specifically designed for students in higher education. Your primary goal is to provide empathetic, judgment-free support during times of stress and mental disturbance.

YOUR EXPERTISE:
- Academic stress and exam anxiety
- Time management and procrastination
- Social anxiety and difficulty speaking up
- Career tension and future planning anxiety
- Fear of rejection and low self-esteem
- Motivation and finding purpose

YOUR APPROACH:
- Be warm, understanding, and conversational
- Validate their feelings before offering suggestions
- Provide practical, actionable advice
- Offer coping strategies and reframing techniques
- Keep responses concise but thorough (2-4 paragraphs typically)
- Never dismiss feelings with oversimplified advice like "just go outside" or "it's not that bad"

CRITICAL BOUNDARIES:
- You are NOT a replacement for professional therapy or counseling
- You cannot diagnose mental health conditions
- You cannot prescribe or recommend medication
- When issues seem beyond peer support (severe depression, trauma, abuse), strongly encourage professional help
- If someone mentions suicide, self-harm, or being in danger, IMMEDIATELY provide crisis resources

CRISIS PROTOCOL:
If the user mentions suicide, self-harm, harming others, or being in immediate danger:
- Respond with deep empathy and validate their pain
- Let them know help is available and they don't have to face this alone
- Encourage them to reach out to crisis resources (the application will provide specific numbers)
- Encourage them to reach out to campus counseling services
- DO NOT list specific phone numbers in your response (the system will provide these separately)

Remember: Your role is to provide immediate emotional support while the system provides crisis resources.
"""

# Crisis Resources
CRISIS_RESOURCES = {
    "india": [
        {"name": "Vandrevala Foundation", "number": "+91 9999 666 555", "available": "24/7"},
        {"name": "AASRA", "number": "+91 22 2754 6669", "available": "24/7"},
        {"name": "iCall", "number": "+91 22 2556 3291", "available": "Mon-Sat, 8am-10pm"}
    ]
}

# load api key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# config arcee
genai.configure(api_key=GEMINI_API_KEY) #type: ignore

model = genai.GenerativeModel( #type: ignore
    model_name='gemini-2.5-flash-lite',
    system_instruction=SYSTEM_INSTRUCTIONS,
    generation_config={
        'temperature': 0.7,
        'max_output_tokens': 1000
    }
)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Arcee is running!',
        'timestamp': datetime.now().isoformat()
    })

def detect_crisis(text):
    crisis_triggers = [
        # self-harm and suicide
        "suicide", "kill myself", "end it all", "want to die",
        "better off dead", "no reason to live", "end my life",
        "suicida", "hurt myself", "cut myself",

        # depression and hopelessness
        "can't go on", "can't take it anymore", "hopeless", 
        "nothing matters",

        # abuse
        "abuse", "being abused", "domestic violence", "rape"
        , "sexual assault", "trapped",

        # emergency situations
        "going to kill myself", "going to end it", "final goodbye",
        "goodbye forever", "last message", "ending my life"
    ]

    text_lower = text.lower()

    for trigger in crisis_triggers:
        if trigger in text_lower:
            return True
        

    return False

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Request must be JSON'
            }), 400
        
        data = request.get_json()
        message = data.get('message', '').strip()

        if not message:
            return jsonify({
                'success': False,
                'error': 'Message is required and cannot be empty'
            }), 400
        
        is_crisis = detect_crisis(message)

        # Always get arcee's response for both crisis and non crisis situations
        try:
            response = model.generate_content(message)
            arcee_response = response.text

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f"Gemini API error: {str(e)}"
                }), 500
        
        # format response / will handle it in frontend
        if is_crisis:
            response_data = {
                'success': True,
                'response': arcee_response,
                'is_crisis': True,
                'crisis_resources': CRISIS_RESOURCES['india']
            }
        else:
            response_data = {
                'success': True,
                'is_crisis': False,
                'response': arcee_response
            }

        # Return json response
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Server error: {str(e)}"
        }), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)


## Currently keeping the backend stateless will add later in the frontend