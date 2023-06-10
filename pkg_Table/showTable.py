

## SQL데이터 DataFrame을 이용하여 Treeview에 기록하여 출력.
class ShowTable(object):
    def fn_show_table(selected_DBtable, df=None, extra=None):
        try:
            n_root = tkinter.Toplevel()
            n_root.title(f"{database}  //  {selected_DBtable}")
            n_root.geometry("1850x1000")

            # Add some style
            style = ttk.Style()
            # Pick a theme
            style.theme_use("default")

            # Configure our treeview colors
            style.configure("Treeview",
                            background="#D3D3D3",
                            foreground="black",
                            rowheight=25,
                            fieldbackground="#D3D3D3"
                            )
            # Change selected color
            style.map('Treeview',
                      background=[('selected', '#347083')])

            btn_view = Button(n_root, width=15, height=2, text='To_Excel', command=lambda: df.to_excel('123.csv'))
            btn_view.place(x=35, y=5)

            # Create Treeview Frame
            frame1 = Frame(n_root, relief="solid", bd=2)
            frame1.pack(pady=50, fill="both", expand=True)

            # frame1 = Frame(n_root)
            # frame1.pack(pady=10)

            tree_scroll_y = Scrollbar(frame1, orient="vertical")
            tree_scroll_y.pack(side=RIGHT, fill=Y)
            tree_scroll_x = Scrollbar(frame1, orient="horizontal")
            tree_scroll_x.pack(side=BOTTOM, fill=X)

            my_tree = ttk.Treeview(frame1, style="Treeview", height=35, yscrollcommand=tree_scroll_y.set,
                                   xscrollcommand=tree_scroll_x.set, selectmode="extended")
            # Pack to the screen
            my_tree.pack()

            tree_scroll_y.config(command=my_tree.yview)
            tree_scroll_x.config(command=my_tree.xview)

            my_tree["column"] = list(df.columns)
            my_tree["show"] = "headings"

            # Loop thru column list for headers
            for column in my_tree["column"]:
                my_tree.column(column, width=90, minwidth=90)
                my_tree.heading(column, text=column)

            my_tree.tag_configure('oddrow', background="lightblue")
            my_tree.tag_configure('evenrow', background="white")

            # Put data in treeview
            df_rows = df.round(3)
            df_rows = df_rows.to_numpy().tolist()

            global count
            count = 0
            for row in df_rows:
                if count % 2 == 0:
                    my_tree.insert(parent='', index='end', iid=count, text="", values=row, tags=('evenrow',))
                else:
                    my_tree.insert(parent='', index='end', iid=count, text="", values=row, tags=('oddrow',))
                count += 1

            if (extra is not None):
                frame2 = Frame(n_root, relief="solid", bd=2)
                frame2.pack(side="bottom", fill="both", expand=True, pady=10)

                my_tree_extra = ttk.Treeview(frame2)

                my_tree_extra["column"] = list(extra.columns)
                my_tree_extra["show"] = "headings"

                # Loop thru column list for headers
                for column in my_tree_extra["column"]:
                    my_tree_extra.column(column, width=110, minwidth=110)
                    my_tree_extra.heading(column, text=column)

                # Put data in treeview
                df_rows = extra.to_numpy().tolist()
                for row in df_rows:
                    my_tree_extra.insert("", "end", values=row)

                my_tree_extra.pack(pady=20)

            # n_root.mainloop()

        except:
            print('fn_show_table')
