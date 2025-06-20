import pygame

class Card:
    def __init__(self, option, description, width, height):
        self.option = option
        self.description = description
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

    def draw(self, screen, selected):
        if selected:
            pygame.draw.rect(self.surface, (255, 255, 0, 128), self.surface.get_rect())
        else:
            pygame.draw.rect(self.surface, (200, 200, 200, 128), self.surface.get_rect())

        # Render the option text with a black outline
        option_font = pygame.font.Font(None, 24)
        option_lines = self.wrap_text(self.option, option_font, self.width - 20)
        option_y = 20
        for line in option_lines:
            line_surface = self.render_text_with_outline(line, option_font, (255, 255, 255), (0, 0, 0))
            line_rect = line_surface.get_rect(centerx=self.surface.get_width() // 2, top=option_y)
            self.surface.blit(line_surface, line_rect)
            option_y += line_rect.height + 5

        # Render the description text with a black outline
        description_font = pygame.font.Font(None, 18)
        description_lines = self.wrap_text(self.description, description_font, self.width - 20)
        description_y = option_y + 20
        for line in description_lines:
            line_surface = self.render_text_with_outline(line, description_font, (255, 255, 255), (0, 0, 0))
            line_rect = line_surface.get_rect(centerx=self.surface.get_width() // 2, top=description_y)
            self.surface.blit(line_surface, line_rect)
            description_y += line_rect.height + 5

        screen.blit(self.surface, self.rect)

    def render_text_with_outline(self, text, font, color, outline_color):
        outline_surface = font.render(text, True, outline_color)
        text_surface = font.render(text, True, color)

        final_surface = pygame.Surface(outline_surface.get_size(), pygame.SRCALPHA)

        # Draw the outline by blitting the outline_surface at slight offsets
        final_surface.blit(outline_surface, (-1, -1))
        final_surface.blit(outline_surface, (-1, 1))
        final_surface.blit(outline_surface, (1, -1))
        final_surface.blit(outline_surface, (1, 1))

        # Draw the text on top of the outline
        final_surface.blit(text_surface, (0, 0))

        return final_surface

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_width = font.size(test_line)[0]

            if test_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines