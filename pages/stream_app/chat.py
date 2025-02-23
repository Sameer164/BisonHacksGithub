# from typing import Union

# import humanize
# import streamlit as st
# from langchain_core.runnables import RunnableConfig

# from open_notebook.domain.base import ObjectModel
# from open_notebook.domain.notebook import ChatSession, Note, Notebook, Source
# from open_notebook.graphs.chat import graph as chat_graph
# # from open_notebook.plugins.podcasts import PodcastConfig
# from open_notebook.utils import token_count
# from pages.stream_app.utils import (
#     convert_source_references,
#     create_session_for_notebook,
# )

# from .note import make_note_from_chat


# # todo: build a smarter, more robust context manager function
# def build_context(notebook_id):
#     st.session_state[notebook_id]["context"] = dict(note=[], source=[])

#     for id, status in st.session_state[notebook_id]["context_config"].items():
#         if not id:
#             continue

#         item_type, item_id = id.split(":")
#         if item_type not in ["note", "source"]:
#             continue

#         if "not in" in status:
#             continue

#         try:
#             item: Union[Note, Source] = ObjectModel.get(id)
#         except Exception:
#             continue

#         if "insights" in status:
#             st.session_state[notebook_id]["context"][item_type] += [
#                 item.get_context(context_size="short")
#             ]
#         elif "full content" in status:
#             st.session_state[notebook_id]["context"][item_type] += [
#                 item.get_context(context_size="long")
#             ]

#     return st.session_state[notebook_id]["context"]


# def execute_chat(txt_input, context, current_session):
#     current_state = st.session_state[current_session.id]
#     current_state["messages"] += [txt_input]
#     current_state["context"] = context
#     result = chat_graph.invoke(
#         input=current_state,
#         config=RunnableConfig(configurable={"thread_id": current_session.id}),
#     )
#     current_session.save()
#     return result


# def chat_sidebar(current_notebook: Notebook, current_session: ChatSession):
#     context = build_context(notebook_id=current_notebook.id)
#     tokens = token_count(
#         str(context) + str(st.session_state[current_session.id]["messages"])
#     )
#     chat_tab, podcast_tab = st.tabs(["Chat", "Podcast"])
#     with st.expander(f"Context ({tokens} tokens), {len(str(context))} chars"):
#         st.json(context)
#     with chat_tab:
#         with st.expander(
#             f"**Session:** {current_session.title} - {humanize.naturaltime(current_session.updated)}"
#         ):
#             new_session_name = st.text_input(
#                 "Current Session",
#                 key="new_session_name",
#                 value=current_session.title,
#             )
#             c1, c2 = st.columns(2)
#             if c1.button("Rename", key="rename_session"):
#                 current_session.title = new_session_name
#                 current_session.save()
#                 st.rerun()
#             if c2.button("Delete", key="delete_session_1"):
#                 current_session.delete()
#                 st.session_state[current_notebook.id]["active_session"] = None
#                 st.rerun()
#             st.divider()
#             new_session_name = st.text_input(
#                 "New Session Name",
#                 key="new_session_name_f",
#                 placeholder="Enter a name for the new session...",
#             )
#             st.caption("If no name provided, we'll use the current date.")
#             if st.button("Create New Session", key="create_new_session"):
#                 new_session = create_session_for_notebook(
#                     notebook_id=current_notebook.id, session_name=new_session_name
#                 )
#                 st.session_state[current_notebook.id]["active_session"] = new_session.id
#                 st.rerun()
#             st.divider()
#             sessions = current_notebook.chat_sessions
#             if len(sessions) > 1:
#                 st.markdown("**Other Sessions:**")
#                 for session in sessions:
#                     if session.id == current_session.id:
#                         continue

#                     st.markdown(
#                         f"{session.title} - {humanize.naturaltime(session.updated)}"
#                     )
#                     if st.button(label="Load", key=f"load_session_{session.id}"):
#                         st.session_state[current_notebook.id]["active_session"] = (
#                             session.id
#                         )
#                         st.rerun()
#         with st.container(border=True):
#             request = st.chat_input("Enter your question")
#             # removing for now since it's not multi-model capable right now
#             if request:
#                 response = execute_chat(
#                     txt_input=request,
#                     context=context,
#                     current_session=current_session,
#                 )
#                 st.session_state[current_session.id]["messages"] = response["messages"]

#             for msg in st.session_state[current_session.id]["messages"][::-1]:
#                 if msg.type not in ["human", "ai"]:
#                     continue
#                 if not msg.content:
#                     continue

#                 with st.chat_message(name=msg.type):
#                     st.markdown(convert_source_references(msg.content))
#                     if msg.type == "ai":
#                         if st.button("💾 New Note", key=f"render_save_{msg.id}"):
#                             make_note_from_chat(
#                                 content=msg.content,
#                                 notebook_id=current_notebook.id,
#                             )
#                             st.rerun()

from typing import Union

import humanize
import streamlit as st
from langchain_core.runnables import RunnableConfig

from open_notebook.domain.base import ObjectModel
from open_notebook.domain.notebook import ChatSession, Note, Notebook, Source
from open_notebook.graphs.chat import graph as chat_graph
# from open_notebook.plugins.podcasts import PodcastConfig
from open_notebook.utils import token_count
from pages.stream_app.utils import (
    convert_source_references,
    create_session_for_notebook,
)

from .note import make_note_from_chat


# todo: build a smarter, more robust context manager function
def build_context(notebook_id):
    st.session_state[notebook_id]["context"] = dict(note=[], source=[])

    for id, status in st.session_state[notebook_id]["context_config"].items():
        if not id:
            continue

        item_type, item_id = id.split(":")
        if item_type not in ["note", "source"]:
            continue

        if "not in" in status:
            continue

        try:
            item: Union[Note, Source] = ObjectModel.get(id)
        except Exception:
            continue

        if "insights" in status:
            st.session_state[notebook_id]["context"][item_type] += [
                item.get_context(context_size="short")
            ]
        elif "full content" in status:
            st.session_state[notebook_id]["context"][item_type] += [
                item.get_context(context_size="long")
            ]

    return st.session_state[notebook_id]["context"]


def execute_chat(txt_input, context, current_session):
    current_state = st.session_state[current_session.id]
    current_state["messages"] += [txt_input]
    current_state["context"] = context
    result = chat_graph.invoke(
        input=current_state,
        config=RunnableConfig(configurable={"thread_id": current_session.id}),
    )
    current_session.save()
    return result


def chat_sidebar(current_notebook: Notebook, current_session: ChatSession):
    context = build_context(notebook_id=current_notebook.id)
    tokens = token_count(
        str(context) + str(st.session_state[current_session.id]["messages"])
    )
    # Remove the Podcast tab by creating only a single "Chat" tab.
    chat_tab = st.tabs(["Chat"])[0]
    with st.expander(f"Context ({tokens} tokens), {len(str(context))} chars"):
        st.json(context)
    with chat_tab:
        with st.expander(
            f"**Session:** {current_session.title} - {humanize.naturaltime(current_session.updated)}"
        ):
            new_session_name = st.text_input(
                "Current Session",
                key="new_session_name",
                value=current_session.title,
            )
            c1, c2 = st.columns(2)
            if c1.button("Rename", key="rename_session"):
                current_session.title = new_session_name
                current_session.save()
                st.rerun()
            if c2.button("Delete", key="delete_session_1"):
                current_session.delete()
                st.session_state[current_notebook.id]["active_session"] = None
                st.rerun()
            st.divider()
            new_session_name = st.text_input(
                "New Session Name",
                key="new_session_name_f",
                placeholder="Enter a name for the new session...",
            )
            st.caption("If no name provided, we'll use the current date.")
            if st.button("Create New Session", key="create_new_session"):
                new_session = create_session_for_notebook(
                    notebook_id=current_notebook.id, session_name=new_session_name
                )
                st.session_state[current_notebook.id]["active_session"] = new_session.id
                st.rerun()
            st.divider()
            sessions = current_notebook.chat_sessions
            if len(sessions) > 1:
                st.markdown("**Other Sessions:**")
                for session in sessions:
                    if session.id == current_session.id:
                        continue

                    st.markdown(
                        f"{session.title} - {humanize.naturaltime(session.updated)}"
                    )
                    if st.button(label="Load", key=f"load_session_{session.id}"):
                        st.session_state[current_notebook.id]["active_session"] = (
                            session.id
                        )
                        st.rerun()
        with st.container(border=True):
            request = st.chat_input("Enter your question")
            if request:
                response = execute_chat(
                    txt_input=request,
                    context=context,
                    current_session=current_session,
                )
                st.session_state[current_session.id]["messages"] = response["messages"]

            for msg in st.session_state[current_session.id]["messages"][::-1]:
                if msg.type not in ["human", "ai"]:
                    continue
                if not msg.content:
                    continue

                with st.chat_message(name=msg.type):
                    st.markdown(convert_source_references(msg.content))
                    if msg.type == "ai":
                        if st.button("💾 New Note", key=f"render_save_{msg.id}"):
                            make_note_from_chat(
                                content=msg.content,
                                notebook_id=current_notebook.id,
                            )
                            st.rerun()

