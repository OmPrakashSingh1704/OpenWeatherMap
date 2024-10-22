import random

import huggingface_hub

# Initialize the InferenceClient for Hugging Face
client = huggingface_hub.InferenceClient()


def send_warning(user: str, city: str, temperature_threshold: float = 35) -> str:
    """Generate a warning message for a given city and temperature.

    Parameters
    ----------
    user : str
        The user to whom the warning is intended.
    city : str
        The city for which the warning is generated.
    temperature_threshold : float, optional
        The temperature above which the warning should be generated, by default 35.

    Returns
    -------
    str
        The generated warning message.
    """
    # Generate warning text with the grammar constraints
    response = client.chat_completion(
        messages=[
            {"role": "system",
             "content": "You will write a simple and short warning for the given city and temperature."},
            {"role": "user", "content": f"User: {user}\nCity: {city}\nTemperature: {temperature_threshold}"}
        ],
        max_tokens=1000,
        temperature=0.5
    )

    return response.choices[0].message.content


def send_summary(
        City: str, DateTime: str, avg_temp: float, max_temp: float, min_temp: float, dominant_weather: str,
        User: str = 'Visitor'
) -> str:
    """Generate a weather summary for a given city and temperature.

    Parameters
    ----------
    City : str
        The city for which the summary is generated.
    DateTime : str
        The date and time for which the summary is generated.
    avg_temp : float
        The average temperature.
    max_temp : float
        The maximum temperature.
    min_temp : float
        The minimum temperature.
    dominant_weather : str
        The dominant weather status.
    User : str, optional
        The user to whom the summary is intended, by default 'Visitor'.

    Returns
    -------
    str
        The generated summary message.
    """
    # Ensure the keys match
    response = client.chat_completion(
        messages=[
            {"role": "system", "content": "You will write a short summary for the given city and temperature"},
            {
                "role": "user",
                "content": f"User:{User}\n City: {City}\nAverage Temperature: {avg_temp}\nMaximum Temperature: {max_temp}\nMinimum Temperature: {min_temp}\nDominant Weather: {dominant_weather}\nDate and Time: {DateTime}"
            },
        ],
        max_tokens=1000,
        temperature=0.5,
        seed=random.randint(0, 2 ** 32 - 1),  # Ensure the output is different each time
    )

    return response.choices[0].message.content
