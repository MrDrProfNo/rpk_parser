from tkinter import *
from tkinter import ttk
from typing import List
from rpk_searchutils import scan_mem_ref as scan
from rpk_searchutils import OffsetResults

from traceback import print_exc

DISPLAY_LINE_WIDTH = 64


class ByteScanner:
    def __init__(self, root):

        self.offset_results: List[OffsetResults] = []
        self.byte_frame_labels = []

        root.title("ByteScanner")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.path_text = StringVar()
        self.path_text.set("../rpks/test_rpk.rpk")
        path_entry = ttk.Entry(mainframe, width=20, textvariable=self.path_text)
        path_entry.grid(column=2, row=1, sticky=(W, E))

        self.byte_frame = ttk.Frame(root, padding="10 10 10 10")
        self.byte_frame.grid(column=0, row=1, sticky=(S, W))
        root.rowconfigure(1, weight=1)

        ttk.Button(mainframe, text="Load", command=self.load_onclick).grid(column=3, row=3, sticky=W)

        ttk.Label(mainframe, text="path").grid(column=1, row=1, sticky=E)

        path_entry.focus()
        root.bind("<Return>", self.load_onclick)

    def load_onclick(self, *args) -> None:
        print(f"got *args: {args}")

        try:
            with open(self.path_text.get(), "rb") as f:
                contents = f.read()
        except IOError:
            print_exc()
        else:
            self.offset_results = scan.find_offsets(contents)
            self.display_bytes(contents)

    def get_references_me(self, bytepos, contents: List[OffsetResults]):
        references_ord_32 = []
        references_offset_32 = []
        references_ord_64 = []
        references_offset_64 = []

        for idx, offsetResult in enumerate(contents):
            if offsetResult.offset_32bit == bytepos:
                references_ord_32.append(idx)

            if offsetResult.offset_rel_32bit == bytepos:
                references_offset_32.append(idx)

            if offsetResult.offset_64bit == bytepos:
                references_ord_64.append(idx)

            if offsetResult.offset_rel_64bit == bytepos:
                references_offset_64.append(idx)

        return (references_ord_32,
                references_offset_32,
                references_ord_64,
                references_offset_64)


    def display_bytes(self, contents: bytes):
    
        # delete whatever was in the grid before
        for row in self.byte_frame.winfo_children():
            for column in row.winfo_children():
                column.destroy()
            row.destroy()

        self.byte_frame_labels = []

    
        line_count = len(contents) // DISPLAY_LINE_WIDTH
        last_line_len = len(contents) % DISPLAY_LINE_WIDTH
    
        ttk.Style().configure('cellOnHover.TLabel', background='blue')
        ttk.Style().configure('cellRef32.TLabel', background='red')
    
        # loop over line_count, +1 for the partial line at the end.
        for row_number in range(0, line_count + 1):
            first_byte = row_number * DISPLAY_LINE_WIDTH
            row_frame = ttk.Frame(self.byte_frame, padding="0 0 0 0")
            row_frame.grid(row=row_number, column=1, sticky=(W,))
            for col_number, byte in enumerate(contents[first_byte: first_byte + DISPLAY_LINE_WIDTH]):
                cell_label = ttk.Label(row_frame, padding="2 2 2 2", text=f"{byte:<02x}")
                cell_label.grid(row=0, column=col_number)

                self.byte_frame_labels.append(cell_label)

                def cell_on_enter(*args, current, row_number, col_number):
                    current.configure(style='cellOnHover.TLabel')
                    references = self.get_references_me(row_number * DISPLAY_LINE_WIDTH + col_number,
                                                        self.offset_results)

                    for ref_32_idx in references[1]:
                        self.byte_frame_labels[ref_32_idx].configure(style='cellRef32.TLabel')

                def cell_on_leave(*args, current, row_number, col_number):
                    current.configure(style='TLabel')
                    references = self.get_references_me(row_number * DISPLAY_LINE_WIDTH + col_number,
                                                        self.offset_results)

                    for ref_32_idx in references[1]:
                        self.byte_frame_labels[ref_32_idx].configure(style='TLabel')

                cell_label.bind('<Enter>',
                                lambda *args, current=cell_label, row_number=row_number,
                                       col_number=col_number: cell_on_enter(
                                    *args,
                                    current=current,
                                    row_number=row_number,
                                    col_number=col_number))
                cell_label.bind('<Leave>',
                                lambda *args, current=cell_label, row_number=row_number,
                                       col_number=col_number: cell_on_leave(
                                    *args,
                                    current=current,
                                    row_number=row_number,
                                    col_number=col_number))


def main():
    root = Tk()
    ByteScanner(root)
    root.mainloop()


if __name__ == "__main__":
    main()


