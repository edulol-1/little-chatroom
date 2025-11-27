import curses
import sys
from curses.textpad import Textbox, rectangle

class InterfaceHandler:
    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(1)
        
        # Set the size of all the upper part of the interface
        self.upper_rect_h = int(curses.LINES * 0.8)
        self.upper_rect_w = int(curses.COLS * 0.99)
        self.lower_rect_h = int(curses.LINES * 0.2)
        self.lower_rect_w = self.upper_rect_w

        self.out_messages_win_h = int(curses.LINES * 0.73)
        self.out_messages_win_w = int(curses.COLS * 0.9)
        self.out_messages_win_uly = int(curses.LINES * 0.07)
        self.out_messages_win_ulx = int(curses.COLS * 0.05)

        self.messages_win_h = int(curses.LINES * 0.65)
        self.messages_win_w = int(curses.COLS * 0.8)
        self.messages_win_uly = int(curses.LINES * 0.1)
        self.messages_win_ulx = int(curses.COLS * 0.1)

        # Set the size of the rectangle and the windows in the lower part
        self.out_chat_win_h = int(curses.LINES * 0.17)
        self.out_chat_win_w = int(curses.COLS * 0.9)
        self.out_chat_win_uly = int(curses.LINES * (0.8 + 0.05))
        self.out_chat_win_ulx = int(curses.COLS * 0.05)

        self.chat_win_h = int(curses.LINES * 0.09)
        self.chat_win_w = int(curses.COLS * 0.8)
        self.chat_win_uly = int(curses.LINES * (0.8 + 0.08))
        self.chat_win_ulx = int(curses.COLS * 0.1)

        self.out_messages_win = None
        self.out_chat_win = None
        self.messages_win = None
        self.chat_win = None
        self.textbox = None

    def set_rectangles(self):
        rectangle(self.screen, 0, 0, self.upper_rect_h, self.upper_rect_w)
        rectangle(self.screen, self.upper_rect_h, 0, self.upper_rect_h + self.lower_rect_h, self.lower_rect_w)
        self.screen.refresh()

    def set_windows(self):
        self.messages_win = curses.newwin(self.messages_win_h, self.messages_win_w,
                                          self.messages_win_uly, self.messages_win_ulx)
        self.out_messages_win = curses.newwin(self.out_messages_win_h, self.out_messages_win_w,
                                                  self.out_messages_win_uly, self.out_messages_win_ulx)
        self.chat_win = curses.newwin(self.chat_win_h, self.chat_win_w,
                                      self.chat_win_uly, self.chat_win_ulx)
        self.out_chat_win = curses.newwin(self.out_chat_win_h, self.out_chat_win_w,
                                          self.out_chat_win_uly, self.out_chat_win_ulx)
        self.out_messages_win.border("|", "|", "-", "-", "+", "+", "+", "+")
        self.out_chat_win.border("|", "|", "-", "-", "+", "+", "+", "+")
        self.messages_win.scrollok(True)
        self.messages_win.refresh()
        self.out_messages_win.refresh()
        self.chat_win.nodelay(True)
        self.chat_win.refresh()
        self.out_chat_win.refresh()

    def set_chatbox1(self):
        self.textbox = Textbox(self.chat_win)

    def clear_chatbox(self):
        self.chat_win.clear()
        self.chat_win.refresh()

    def set_chatbox(self):
        while True:
            self.textbox = Textbox(self.chat_win)
            self.textbox.edit()
            outgoing_msg = self.textbox.gather()
            self.chat_win.clear()
            line_count = outgoing_msg.count("\n")
            self.print_message(line_count, outgoing_msg)
            self.chat_win.refresh()

    def type_and_get_message(self):
        self.textbox = Textbox(self.chat_win)
        self.textbox.edit()
        outgoing_msg = self.textbox.gather()
        self.chat_win.clear()
        self.chat_win.refresh()
        return outgoing_msg

    def type_and_get_ch(self):
        return self.chat_win.getch()

    def clear_chat_win(self):
        self.chat_win.clear()
        #self.chat_win.refresh()

    def buffer_to_chat(self, buff):
        self.chat_win.addstr(0, 0, buff)

    def print_message(self, message):
        line_count = message.count("\n")
        line_count = line_count if line_count > 0 else 1
        self.messages_win.scroll(line_count + 1)
        self.messages_win.refresh()
        self.messages_win.addstr(self.messages_win_h - line_count, 0, message)
        self.messages_win.refresh()
        self.out_messages_win.refresh()

    def close(self):
        curses.napms(2000)
        curses.echo()
        curses.endwin()

    def launch_interface(self):
        self.set_rectangles()
        self.set_windows()
        self.set_chatbox1()

# if __name__ == "__main__":
#     interface = InterfaceHandler()
#     interface.launch_interface()
#     input_buffer = ""
#     while True:
#         ch = interface.type_and_get_ch()

#         if ch == -1:
#             continue
#         if ch in (10, 13):
#         #if ch == 7:
#             interface.print_message(input_buffer)
#             input_buffer = ""
#             interface.clear_chat_win()
#         elif ch in (curses.KEY_BACKSPACE, 8, 127):
#             input_buffer = input_buffer[:-1]
#             interface.clear_chat_win()
#             interface.buffer_to_chat(input_buffer)
#         else:
#             input_buffer += chr(ch)
#             interface.buffer_to_chat(input_buffer)
#     interface.close()
