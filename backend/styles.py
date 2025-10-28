from models import StyleConfig

# Conversation styles inspired by Claude
CONVERSATION_STYLES = {
    "default": StyleConfig(
        name="default",
        display_name="Balanced",
        system_prompt="You are a helpful AI assistant. Provide clear, accurate, and concise responses.",
        description="Balanced responses suitable for general questions"
    ),
    "concise": StyleConfig(
        name="concise",
        display_name="Concise",
        system_prompt="You are a helpful AI assistant. Provide brief, direct answers. Be concise and to the point. Avoid unnecessary elaboration.",
        description="Brief and direct answers"
    ),
    "explanatory": StyleConfig(
        name="explanatory",
        display_name="Explanatory",
        system_prompt="You are a helpful AI assistant. Provide detailed, thorough explanations. Break down complex topics into understandable parts. Include examples and context where helpful.",
        description="Detailed explanations with examples"
    ),
    "formal": StyleConfig(
        name="formal",
        display_name="Formal",
        system_prompt="You are a professional AI assistant. Provide responses in a formal, academic tone. Use precise language and maintain professional standards.",
        description="Professional and academic tone"
    ),
    "creative": StyleConfig(
        name="creative",
        display_name="Creative",
        system_prompt="You are a creative AI assistant. Feel free to think outside the box, use analogies, and provide engaging, imaginative responses while remaining accurate and helpful.",
        description="Creative and engaging responses"
    ),
    "research": StyleConfig(
        name="research",
        display_name="Research",
        system_prompt="You are a research-focused AI assistant. Provide evidence-based, well-sourced responses. When using search results, cite sources clearly. Be thorough and analytical.",
        description="Evidence-based with source citations"
    ),
}


def get_style(style_name: str) -> StyleConfig:
    """Get a conversation style by name, defaulting to 'default' if not found."""
    return CONVERSATION_STYLES.get(style_name, CONVERSATION_STYLES["default"])


def get_all_styles() -> dict[str, StyleConfig]:
    """Get all available conversation styles."""
    return CONVERSATION_STYLES
