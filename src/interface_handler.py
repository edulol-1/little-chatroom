import curses
import sys
from curses.textpad import Textbox, rectangle

class InterfaceHandler:
    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
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
        self.chat_win.refresh()
        self.out_chat_win.refresh()

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

    def print_message(self, message):
        line_count = message.count("\n")
        self.messages_win.scroll(line_count)
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

    def start_interface(self):
        try:
            self.set_rectangles()
            self.set_windows()
            #self.set_chatbox()
        except KeyboardInterrupt:
            print("See you later my friend!\n")
        except Exception as err:
            print(type(err))
            print(f"XD {err}")
            print("Terminal should be at least 100x33 in size!")
        finally:
            self.close()
            #curses.napms(2000)
            #curses.echo()
            #curses.endwin()
