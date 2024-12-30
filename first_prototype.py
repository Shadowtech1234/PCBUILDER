import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PC Builder")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 122, 255)
LIGHT_BLUE = (173, 216, 230)

# Fonts
font = pygame.font.Font(None, 36)

# Load the icon image
icon = pygame.image.load('pc.png')  # Replace 'pc.png' with your image file
pygame.display.set_icon(icon)

# PC parts
components = {
    "Games": ["Fortnite", "Minecraft", "Rocket League", "Roblox"],
    "FPS": ["60", "120", "180", "240"],
    "Graphics": ["Low", "Medium", "High"],
}
selected_parts = {"Games": None, "FPS": None, "Graphics": None}

# Scrollable surface dimensions
scrollable_height = 1600  # Increase the height to create a scrollable area
scrollable_surface = pygame.Surface((WIDTH, scrollable_height))

# Scroll variables
scroll_y = 0
scroll_speed = 20

# Buttons and menu configuration
button_width, button_height = 200, 50
menu_x, menu_y = 50, 35
spacing = 60

# Function to draw buttons for a component
def draw_buttons(component_name, options, start_y):
    y_offset = start_y
    for option in options:
        button_rect = pygame.Rect(menu_x, y_offset, button_width, button_height)
        pygame.draw.rect(scrollable_surface, GRAY, button_rect)
        text = font.render(option, True, BLACK)
        scrollable_surface.blit(text, (menu_x + 10, y_offset + 10))
        y_offset += spacing
    return options

# Function to draw the configuration
def draw_configuration():
    x_offset, y_offset = 400, 100
    scrollable_surface.blit(font.render("Selected Settings:", True, BLACK), (x_offset, y_offset))
    for key, value in selected_parts.items():
        y_offset += 40
        text = f"{key}: {value if value else 'Not selected'}"
        scrollable_surface.blit(font.render(text, True, BLACK), (x_offset, y_offset))

# Function to handle selection
def handle_selection(pos, component_name, options, start_y):
    global selected_parts
    y_offset = start_y
    for option in options:
        button_rect = pygame.Rect(menu_x, y_offset, button_width, button_height)
        if button_rect.collidepoint(pos):
            selected_parts[component_name] = option
            return
        y_offset += spacing

# Main loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Adjust mouse_pos for scrolling
            adjusted_pos = (mouse_pos[0], mouse_pos[1] + scroll_y)
            # Check for selection in each component menu
            start_y = menu_y
            for component_name, options in components.items():
                handle_selection(adjusted_pos, component_name, options, start_y)
                start_y += len(options) * spacing + 40  # Adjust start_y for the next menu
        elif event.type == pygame.MOUSEWHEEL:
            scroll_y = max(0, min(scroll_y - event.y * scroll_speed, scrollable_height - HEIGHT))

    # Draw content on the scrollable surface
    scrollable_surface.fill(WHITE)
    start_y = menu_y
    for component_name, options in components.items():
        title = font.render(f"{component_name}:", True, BLACK)
        scrollable_surface.blit(title, (menu_x, start_y - 30))
        draw_buttons(component_name, options, start_y)
        start_y += len(options) * spacing + 40
    draw_configuration()

    # Blit the scrollable surface to the main screen
    screen.blit(scrollable_surface, (0, -scroll_y))

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
