from flask import Flask, render_template_string
from wtforms import SelectMultipleField, Form
from wtforms import widgets

app = Flask(__name__)

data = [('value_a','Value A'), ('value_b','Value B'), ('value_c','Value C')]


class ExampleForm(Form):
    example = SelectMultipleField(
        'Pick Things!',
        choices=data,
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
        )


@app.route('/')
def home():
    form = ExampleForm()
    return render_template_string('<form>{{ form.example }}</form>',form=form)

if __name__ == '__main__':
    app.run(debug=True)