import streamlit as st
import openai
import os
from typing import Dict, Any

# load environment variables from .env (for local development)
from dotenv import load_dotenv
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="vectra - AI Prompt Refiner",
    page_icon="✨",
    layout="centered"
)

# Initialize session state
if 'optimized_prompt' not in st.session_state:
    st.session_state.optimized_prompt = ""
if 'prompt_explanation' not in st.session_state:
    st.session_state.prompt_explanation = ""

def get_openai_client() -> bool:
    """Configure OpenAI API key; returns True if set successfully."""
    api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv('OPENAI_API_KEY')
    if not api_key:
        st.error("❌ API key not found. Please configure OPENAI_API_KEY in your environment or Streamlit secrets.")
        return False
    openai.api_key = api_key
    return True

def create_refinement_prompt(user_input: str, ai_tool: str, tone: str) -> str:
    """Create the system prompt for refining user input"""
    
    tool_instructions = {
        "General AI": "general-purpose AI assistants like ChatGPT",
        "Image Generation": "image generation tools like Midjourney, DALL·E, or Stable Diffusion",
        "Code Generation": "code generation tools like GitHub Copilot or CodeLlama",
        "Marketing Content": "marketing and content creation tools"
    }
    
    tone_instructions = {
        "Professional": "formal, business-oriented, and clear",
        "Creative": "imaginative, artistic, and innovative",
        "Minimal": "concise, simple, and to the point",
        "Cinematic": "dramatic, visually descriptive, and emotionally engaging",
        "Friendly": "casual, approachable, and conversational"
    }
    
    system_prompt = f"""
You are an expert prompt engineer. Your task is to refine user inputs into well-structured, detailed prompts for {tool_instructions[ai_tool]}.

The user wants a {tone_instructions[tone]} tone.

Transform the user's input into a structured prompt with these exact sections:

[ROLE]
Who the AI should act as - be specific about expertise and perspective

[TASK]
Clear description of what to generate - be detailed and specific

[STYLE]
Creative or visual style - describe the aesthetic, mood, and approach

[DETAILS]
Extra specifications, context, audience, tone - include relevant constraints and requirements

[CONSTRAINTS]
Things to avoid or limits - specify what NOT to do or boundaries

Make the prompt comprehensive but not overly verbose. Add missing details that would be helpful for the target AI tool.
"""
    
    return system_prompt

def refine_prompt_with_ai(user_input: str, ai_tool: str, tone: str) -> Dict[str, str]:
    """Send user input to OpenAI for refinement"""
    try:
        system_prompt = create_refinement_prompt(user_input, ai_tool, tone)
        full_prompt = f"{system_prompt}\n\nUser request: {user_input}"

        # use ChatCompletion for more flexible responses
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": full_prompt}]
        )
        refined_text = resp['choices'][0]['message']['content']

        explanation_prompt = (
            f"Based on this refined prompt: {refined_text}\n\n"
            "Provide a brief explanation (2-3 sentences) of why this prompt structure works well for the user's goal. "
            "Focus on how the structure helps the AI understand and execute the task effectively."
        )
        explanation_resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": explanation_prompt}]
        )

        return {
            "prompt": refined_text,
            "explanation": explanation_resp['choices'][0]['message']['content']
        }
    except Exception as e:
        return {
            "prompt": f"Error generating prompt: {str(e)}",
            "explanation": "Please check your API key and try again."
        }

def main():
    """Main application function"""
    
    # App title and description
    st.title("✨ vectra - AI Prompt Refiner")
    st.markdown("*Transform simple ideas into powerful AI prompts*")
    st.markdown("---")
    
    # configure OpenAI client
    if not get_openai_client():
        st.error("❌ API Key Required: Please set your OPENAI_API_KEY in the deployment environment variables/secrets.")
        st.info("For local development, create a `.env` file with `OPENAI_API_KEY=your_key_here`")
        return
    
    # User input section
    st.subheader("📝 Describe what you want to create")
    user_input = st.text_area(
        "Enter your idea in simple English:",
        placeholder="Example: make a logo for a gym brand",
        height=100,
        help="Describe what you want to create in simple, everyday language"
    )
    
    # Configuration columns
    col1, col2 = st.columns(2)
    
    with col1:
        ai_tool = st.selectbox(
            "🎯 AI Tool Optimization:",
            options=["General AI", "Image Generation", "Code Generation", "Marketing Content"],
            help="Choose the type of AI tool you'll use this prompt with"
        )
    
    with col2:
        tone = st.selectbox(
            "🎨 Tone/Style:",
            options=["Professional", "Creative", "Minimal", "Cinematic", "Friendly"],
            help="Choose the tone and style for your prompt"
        )
    
    # Generate button
    generate_button = st.button(
        "✨ Generate Optimized Prompt",
        type="primary",
        use_container_width=True
    )
    
    # Process the request
    if generate_button:
        if not user_input.strip():
            st.error("Please enter a description of what you want to create.")
            return
        
        with st.spinner("🔄 Refining your prompt..."):
            result = refine_prompt_with_ai(user_input, ai_tool, tone)
            st.session_state.optimized_prompt = result["prompt"]
            st.session_state.prompt_explanation = result["explanation"]
    
    # Display results
    if st.session_state.optimized_prompt:
        st.markdown("---")
        st.subheader("🚀 Optimized Prompt")
        
        # Display the optimized prompt
        prompt_container = st.container()
        with prompt_container:
            st.text_area(
                "Your refined prompt:",
                value=st.session_state.optimized_prompt,
                height=300,
                key="optimized_prompt_display",
                help="This structured prompt is ready to use with your chosen AI tool"
            )
        
        # Copy button
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("📋 Copy Prompt", use_container_width=True):
                st.write("Prompt copied to clipboard!")
                # JavaScript for clipboard functionality
                st.markdown("""
                <script>
                navigator.clipboard.writeText(`""" + st.session_state.optimized_prompt.replace("`", "\\`") + """`);
                </script>
                """, unsafe_allow_html=True)
        
        # Explanation section
        st.subheader("💡 Why this prompt works")
        st.info(st.session_state.prompt_explanation)
        
        # Additional tips
        st.markdown("---")
        st.markdown("### 💡 Pro Tips:")
        st.markdown("""
        - **Be specific**: The more details you provide, the better the result
        - **Iterate**: Feel free to refine your prompt multiple times
        - **Experiment**: Try different AI tool optimizations and tones
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.9em;'>"
        "vectra ✨ | Transform ideas into powerful AI prompts"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
