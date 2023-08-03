
def process_signatory_profile(form, not_specified_choice):
    # Get the cleaned data from the form
    cleaned_data = form.cleaned_data
    # Get the value of the custom choice field -> signatory_profile
    signatory_profile = cleaned_data.get('signatory_profile', )

    # Split the value by space (assuming it is formatted as "first_name last_name position")
    first_name, last_name, position = signatory_profile.split()
    if signatory_profile == not_specified_choice:
        first_name, last_name, position = not_specified_choice, '', not_specified_choice

    # Assign the split values to the corresponding fields
    form.instance.signatory_name = f'{first_name} {last_name}'
    form.instance.signatory_position = position
