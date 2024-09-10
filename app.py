import datetime
import streamlit as st
import logging
import inspect

from streamlit_chat import message
from streamlit.components.v1 import html
from streamlit_js_eval import get_geolocation
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage

from src.service.agent.open_weather.weather import (
    OpenWeather,
    get_weather_current_location_tool,
    get_weather_other_location_tool,
)
from src.service.agent.google.google_meeting import GoogleMeeting, booking_meeting_tool
from src.service.agent.geoapify.geoapify import GeoPlaces, get_restaurant_tool
from src.service.agent.coin_market_cap.coin_market_cap import (
    CoinMarketCap,
    get_coin_tool,
)
from src.service.agent.form.form import get_contact_inform, search_product
from src.service.prompt import prompt
from src.service.llm.openai import OpenAIService
from src.service.llm.model import get_model
from src.utils.constant import CONTACT_FORM, OPEN_AI_MODELS, WEATHER_HTML

st.set_page_config(page_title="💬 OpenAI Chatbot")


def prepare_state():
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "How may I assist you today?"}
        ]
    if "google_meeting" not in st.session_state.keys():
        st.session_state.google_meeting = True

    if "open_weather" not in st.session_state.keys():
        st.session_state.open_weather = True

    if "restaurant" not in st.session_state.keys():
        st.session_state.restaurant = True

    if "coin" not in st.session_state.keys():
        st.session_state.coin = True

    if "contact_form" not in st.session_state.keys():
        st.session_state.contact_form = True

    if "location" not in st.session_state.keys():
        st.session_state.location = None

    st.session_state.location = get_geolocation()


def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]


def get_active_tools():
    tools = [search_product]
    if st.session_state.google_meeting:
        tools.append(booking_meeting_tool)
    if st.session_state.open_weather:
        tools.append(get_weather_current_location_tool)
        tools.append(get_weather_other_location_tool)
    if st.session_state.restaurant:
        tools.append(get_restaurant_tool)
    if st.session_state.coin:
        tools.append(get_coin_tool)
    if st.session_state.contact_form:
        tools.append(get_contact_inform)
    return tools


def get_llm_response(llm_messages: list[BaseMessage]) -> AIMessage:
    tools = get_active_tools()

    output: AIMessage = client.chatCompletion(
        message=llm_messages,
        llm_tools=tools,
    )
    return output


def get_llm_messages():
    llm_messages = [
        SystemMessage(
            prompt.ASSISTANT_AI.format(date=datetime.date.today().strftime("%d/%m/%Y"))
        )
    ]
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            llm_messages.append(HumanMessage(dict_message["content"]))
        else:
            llm_messages.append(AIMessage(dict_message["content"]))
    return llm_messages


def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.user_input = ""
    st.session_state.messages.append({"role": "user", "content": user_input})
    llm_messages = get_llm_messages()
    output = get_llm_response(llm_messages)

    logging.info(output)

    if output.tool_calls and len(output.tool_calls) > 0:
        kwargs = output.tool_calls[0]["args"]
        message = _exec_tools(name=output.tool_calls[0]["name"], **kwargs)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": message,
            }
        )
    else:
        st.session_state.messages.append(
            {"role": "assistant", "content": output.content}
        )


def _filter_kwargs(tool_func: callable, **kwargs):
    valid_params = inspect.signature(tool_func).parameters
    filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_params}
    return filtered_kwargs


def _exec_tools(name: str, **kwargs) -> str:
    if name == "booking_meeting_tool":
        agent = GoogleMeeting()
        url = agent.booking_meeting(
            **_filter_kwargs(tool_func=agent.booking_meeting, **kwargs)
        )
        return "I have been created google meeting for you. Link: " + url
    elif name == "get_weather_current_location_tool":
        agent = OpenWeather(st.secrets["OPEN_WEATHER_API_KEY"])
        if st.session_state.location is None:
            return "Please accept location permission"

        (lat, long) = (
            st.session_state.location["coords"]["latitude"],
            st.session_state.location["coords"]["longitude"],
        )
        weather = agent.get_weather(lat, long)
        return agent.convert_markdown(weather)
    elif name == "get_weather_other_location_tool":
        agent = OpenWeather(st.secrets["OPEN_WEATHER_API_KEY"])
        if st.session_state.location is None:
            return "Please accept location permission"
        location = agent.get_location_from_address(address=kwargs["address"])
        if len(location) == 0 or location is None:
            return "No results found"
        lat = location[0]["lat"]
        long = location[0]["lon"]
        weather = agent.get_weather(lat, long)
        return agent.convert_markdown(weather)
    elif name == "get_restaurant_tool":
        agent = GeoPlaces(st.secrets["GEO_API_KEY"])
        if st.session_state.location is None:
            return "Please accept location permission"
        (lat, long) = (
            st.session_state.location["coords"]["latitude"],
            st.session_state.location["coords"]["longitude"],
        )
        json = agent.get_place_restaurant(lat, long, **kwargs)

        llm_messages = [
            SystemMessage(
                prompt.RESTAURANT_AI.format(
                    datetime=datetime.date.today().strftime("%d/%m/%Y %H:%M"),
                    meals=kwargs["meals"],
                    restaurant=json,
                )
            ),
            HumanMessage(list(st.session_state.messages)[-1]["content"]),
        ]
        output: AIMessage = client.chatCompletion(message=llm_messages)
        return output.content
    elif name == "get_coin_tool":
        symbol = kwargs["symbol"]
        agent = CoinMarketCap(st.secrets["COIN_MARKET_CAP_API_KEY"])
        json = agent.get_crypto_currency(
            **_filter_kwargs(tool_func=agent.get_crypto_currency, **kwargs)
        )
        if json["data"][symbol][0] is None:
            return f"Symbol {symbol} not found"
        return agent.convert_markdown(json["data"][kwargs["symbol"]][0])
    elif name == "get_contact_inform":
        return CONTACT_FORM
    elif name == "search_product":
        pass


prepare_state()


# Sidebar
with st.sidebar:
    st.title("💬 OpenAI Chatbot")
    if "OPEN_AI_API_KEY" in st.secrets:
        st.success("API key already provided!", icon="✅")
        open_ai_api = st.secrets["OPEN_AI_API_KEY"]
    else:
        open_ai_api = st.text_input("Enter OpenAI API token:", type="password")
        if not (open_ai_api.startswith("sk-proj")):
            st.warning("Please enter your credentials!", icon="⚠️")
        else:
            st.success("Proceed to entering your prompt message!", icon="👉")

    st.subheader("Models and parameters")
    selected_model = st.sidebar.selectbox(
        "Choose a OpenAI model",
        OPEN_AI_MODELS,
        key="selected_model",
    )
    model = get_model(selected_model)
    temperature = st.sidebar.slider(
        "temperature", min_value=0.01, max_value=1.0, value=0.5, step=0.1
    )
    top_p = st.sidebar.slider(
        "top_p", min_value=0.01, max_value=1.0, value=0.9, step=0.1
    )

    # Location
    st.subheader("Location")

    if st.session_state.location is not None:
        (lat, long) = (
            st.session_state.location["coords"]["latitude"],
            st.session_state.location["coords"]["longitude"],
        )
        st.text(f"Latitude: {lat}\nLongitude: {long}")
    # Agent
    st.subheader("Agents")
    google_meeting = st.checkbox("Google Meeting", value=True, key="google_meeting")
    open_weather = st.checkbox("Weather", value=True, key="open_weather")
    restaurant = st.checkbox("Restaurant", value=True, key="restaurant")
    coin = st.checkbox("Coin Market Cap", value=True, key="coin")
    contact_form = st.checkbox("Show contact form", value=True, key="contact_form")

    configuration = {
        **model,
        "temperature": temperature,
        "top_p": top_p,
        "api_key": open_ai_api,
    }

    client = OpenAIService(**configuration)
    st.sidebar.button("Clear Chat History", on_click=clear_chat_history)

# Chatbot
st.title("CHAT BOT")
chat_placeholder = st.empty()

with chat_placeholder.container():
    for i in range(len(st.session_state.messages)):
        message_chat = st.session_state.messages[i]
        is_user = message_chat["role"] == "user"
        key = "user" if is_user else "assistant"
        with st.chat_message(key):
            st.write(message_chat["content"], unsafe_allow_html=True)


st.text_input("User Input:", on_change=on_input_change, key="user_input")
