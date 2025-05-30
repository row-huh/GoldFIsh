  # Code for generating Pie and Bar charts
  # Code for generating Pie and Bar charts
import matplotlib.pyplot as plt

def generate_pie_chart(df):
    summary = df.groupby("Description")["Amount"].sum()
    fig, ax = plt.subplots()
    ax.pie(summary, labels=summary.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    return fig


def generate_bar_chart(df):
    summary = df.groupby("Description")["Amount"].sum().sort_values()
    fig, ax = plt.subplots()
    summary.plot(kind="barh", ax=ax)
    ax.set_xlabel("Amount")
    ax.set_ylabel("Description")
    ax.set_title("Spending Summary")
    return fig


