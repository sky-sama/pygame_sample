import os
import pygame


os.environ["SDL_IME_SHOW_UI"] = "1"

class Button:
    '''本代码部分由AI生成。被按下时，clicked属性为true。如果按下，并且松手时仍在按钮上，触发callback(无输入)。
    handle_event读取的事件类型：MOUSEBUTTONDOWN，MOUSEBUTTONUP。使用draw绘制。目前不区分左右键。
    '''
    def __init__(self, surface, x, y, width, height, text, font, callback, color=(200,200,200), font_color=(0,0,0), clicked_color=(127,127,127)):
        self.surface=surface
        self.rect = pygame.Rect(x, y, width, height)
        self.text = font.render(text, True, font_color)
        self.color = color
        self.clicked_color=clicked_color
        self.font = font
        self.callback=callback
        self.clicked = False

    def draw(self):
        pygame.draw.rect(self.surface, self.clicked_color if self.clicked else self.color, self.rect)
        self.surface.blit(self.text, (self.rect.x+2, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            if self.clicked and self.rect.collidepoint(event.pos):
                self.callback()
            self.clicked=False
    
    def get_events(self):
        return [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]

class DropDown:
    '''本代码部分由AI生成。实现了基本的下拉框逻辑。
    未经易用性修改。
    '''
    def __init__(self, surface, x, y, width, height, font, options, selected_option_color=(0, 0, 0), option_color=(255, 255, 255), background_color=(200, 200, 200), border_color=(0, 0, 0)):
        self.surface=surface
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.options = options
        self.selected_option = 0
        self.open = False
        self.selected_option_color = selected_option_color
        self.option_color = option_color
        self.background_color = background_color
        self.border_color = border_color

    def draw(self):
        current_option = self.options[self.selected_option]
        pygame.draw.rect(self.surface, self.background_color, self.rect)
        pygame.draw.rect(self.surface, self.border_color, self.rect, 1)
        self.surface.blit(self.font.render(current_option, True, self.selected_option_color), (self.rect.x + 5, self.rect.y + (self.rect.height / 2) - (self.font.get_height() / 2)))

        if self.open:
            for i, option in enumerate(self.options):
                pygame.draw.rect(self.surface, self.background_color, (self.rect.x, self.rect.y + self.rect.height + (i * self.rect.height), self.rect.width, self.rect.height))
                self.surface.blit(self.font.render(option, True, self.option_color if i != self.selected_option else self.selected_option_color), (self.rect.x + 5, self.rect.y + self.rect.height + (i * self.rect.height) + (self.rect.height / 2) - (self.font.get_height() / 2)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.open = not self.open
                return True
            elif self.open:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height + (i * self.rect.height), self.rect.width, self.rect.height)
                    if option_rect.collidepoint(event.pos):
                        self.selected_option = i
                        self.open = False
                        return True
        return False
    
    def get_events(self):
        return [pygame.MOUSEBUTTONDOWN]

class TextInput:
    '''本代码部分由AI生成。实现了基本的文本框逻辑。去选中时调用callback，输入为self。
    handle_event读取的事件类型：KEYDOWN，TEXTINPUT，MOUSEBUTTONDOWN，MOUSEBUTTONUP，MOUSEMOTION。使用draw绘制。目前不区分左右键。
    '''
    def __init__(self, surface, x, y, width, height, font, callback, text_color=(0, 0, 0), select_color=(0, 0, 128), selected_text_color=(255, 255, 255), background_color=(248, 248, 248), border_color=(0, 0, 0), inactive_color=(127, 127, 127)):
        self.surface=surface
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = ''
        self.callback=callback
        self.text_color = text_color
        self.select_color = select_color
        self.selected_text_color = selected_text_color
        self.background_color = background_color
        self.border_color = border_color
        self.inactive_color = inactive_color
        self.active = False  # 是否当前激活输入
        self.cursor_position = 0  # 文本光标位置
        self.selection_start = None  # 文本选择开始位置
        self.mouse_down = False  # 鼠标按下状态

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.callback(self)  # 可以在这里处理回车事件
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    if self.selection_start is not None and self.selection_start != self.cursor_position:
                        self.delete_selection()
                    else:
                        self.text = self.text[:self.cursor_position - 1] + self.text[self.cursor_position:]
                        self.cursor_position = max(0, self.cursor_position - 1)
                        self.selection_start = self.cursor_position
                elif event.key == pygame.K_DELETE:
                    if self.selection_start is not None and self.selection_start != self.cursor_position:
                        self.delete_selection()
                    else:
                        self.text = self.text[:self.cursor_position] + self.text[self.cursor_position + 1:]
                elif event.key == pygame.K_LEFT:
                    if event.mod & pygame.KMOD_SHIFT:
                        self.cursor_position = max(0, self.cursor_position - 1)
                    else:
                        if self.selection_start != self.cursor_position:
                            self.cursor_position = min(self.cursor_position, self.selection_start)
                        else:
                            self.cursor_position = max(0, self.cursor_position - 1)
                        self.selection_start = self.cursor_position
                elif event.key == pygame.K_RIGHT:
                    if event.mod & pygame.KMOD_SHIFT:
                        self.cursor_position = min(len(self.text), self.cursor_position + 1)
                    else:
                        if self.selection_start != self.cursor_position:
                            self.cursor_position = max(self.cursor_position, self.selection_start)
                        else:
                            self.cursor_position = min(len(self.text), self.cursor_position + 1)
                        self.selection_start = self.cursor_position
                '''else:
                    if not(event.mod & pygame.KMOD_SHIFT or event.mod & pygame.KMOD_CTRL or event.mod & pygame.KMOD_ALT):
                        if self.selection_start is not None and self.selection_start != self.cursor_position:
                            self.delete_selection()
                        self.text = self.text[:self.cursor_position] + event.unicode + self.text[self.cursor_position:]
                        self.cursor_position += 1
                        self.selection_start = self.cursor_position'''
        elif event.type == pygame.TEXTINPUT:
            if self.active:
                if self.selection_start is not None and self.selection_start != self.cursor_position:
                    self.delete_selection()
                self.text = self.text[:self.cursor_position] + event.text + self.text[self.cursor_position:]
                self.cursor_position += len(event.text)
                self.selection_start = self.cursor_position
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.mouse_down = True
                self.cursor_position = self.calculate_cursor_position(event.pos)
                self.selection_start = self.cursor_position
            elif self.active:
                self.callback(self)
                self.active = False
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = False
        elif event.type == pygame.MOUSEMOTION:
            if self.mouse_down and self.active:
                self.selection_start = self.calculate_cursor_position(event.pos)

    def draw(self):
        pygame.draw.rect(self.surface, self.background_color, self.rect)

        if self.active:
            pygame.draw.rect(self.surface, self.border_color, self.rect, 1)
            text_surface = self.font.render(self.text, True, self.text_color)
            self.surface.blit(text_surface, (self.rect.x + 5, self.rect.y + (self.rect.height - self.font.get_height()) // 2))
            # 绘制光标
            cursor_pos = self.font.size(self.text[:self.cursor_position])[0] + self.rect.x + 5
            pygame.draw.line(self.surface, self.text_color, (cursor_pos, self.rect.y + 5), (cursor_pos, self.rect.y + self.rect.height - 5))

            # 绘制文本选择
            if self.selection_start is not None and self.selection_start != self.cursor_position:
                if self.selection_start < self.cursor_position:
                    selected_text = self.text[self.selection_start:self.cursor_position]
                    selection_width = self.font.size(selected_text)[0]
                    selection_rect = pygame.Rect(self.rect.x + 5 + self.font.size(self.text[:self.selection_start])[0], self.rect.y, selection_width, self.rect.height)
                else:
                    selected_text = self.text[self.cursor_position:self.selection_start]
                    selection_width = self.font.size(selected_text)[0]
                    selection_rect = pygame.Rect(self.rect.x + 5 + self.font.size(self.text[:self.cursor_position])[0], self.rect.y, selection_width, self.rect.height)
                pygame.draw.rect(self.surface, self.select_color, selection_rect)
                previous_text_width = self.font.size(self.text[:min(self.selection_start, self.cursor_position)])[0]
                selected_text_surface = self.font.render(selected_text, True, self.selected_text_color)
                self.surface.blit(selected_text_surface, (self.rect.x + 5 + previous_text_width, self.rect.y + (self.rect.height - self.font.get_height()) // 2))
        else:  
            pygame.draw.rect(self.surface, self.inactive_color, self.rect, 1)
            text_surface = self.font.render(self.text, True, self.text_color)
            self.surface.blit(text_surface, (self.rect.x + 5, self.rect.y + (self.rect.height - self.font.get_height()) // 2))        

    def calculate_cursor_position(self, pos):
        text_width = self.font.size(self.text)[0]
        if pos[0] < self.rect.x + 5 or pos[0] > self.rect.x + 5 + text_width:
            return len(self.text)
        return int((pos[0] - (self.rect.x + 5)) / (text_width / len(self.text)))

    def delete_selection(self):
        start = min(self.selection_start, self.cursor_position)
        end = max(self.selection_start, self.cursor_position)
        self.text = self.text[:start] + self.text[end:]
        self.cursor_position = start
        self.selection_start = start
        
    def get_events(self):
        return [pygame.KEYDOWN, pygame.TEXTINPUT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]
