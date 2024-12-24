from mpmath import mp
import tkinter as tk

#function to calcualte and display pi
def calculate_pi():
    try:
        precision=int(entry.get())
        if precision < 0 :
            result_label.config(text="Enter a non-negative integer.")
        else: mp.dps = precision + 1
        pi_value=str(mp.pi)
        result_label.config(text=f"Pi to {precision} decimal place is:\n{pi_value}")
    except  ValueError:
        result_label.config(text="Please enter a valide integer")

def clear_all():
    entry.delete(0,tk.END)
    result_label.config(text="")

#Create the main window

root=tk.Tk()
root.title("Petrazteca Pi Calculator")
root.geometry("400x300")

#Message to enter number of decimals

instruction_label=tk.Label(root,text="Enter the number of decimal places for Pi",font=("Arial",12))
instruction_label.pack(pady=10)

# Entry Widget for user input
entry=tk.Entry(root, font=("Arial",12),width=15)
entry.pack(pady=5)

# Button to calculate Pi
Calculate_button=tk.Button(root,text="Calculate Pi",font=("Arial",12),command=calculate_pi)
Calculate_button.pack(pady=10)

# Label to display the result
result_label=tk.Label(root,text="",font=("Arial",12),wraplength=350,justify='center')
result_label.pack(pady=10)

# Button to clear input and results

clear_button=tk.Button(root,text="Clear", font=("Arial",12),command=clear_all)
clear_button.pack(pady=5)


# Run the GUI event loop
root.mainloop()



