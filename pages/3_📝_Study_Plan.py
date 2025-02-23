import asyncio

import streamlit as st

from open_notebook.domain.models import DefaultModels, model_manager
from open_notebook.domain.notebook import Note, Notebook, text_search, vector_search, Source
from open_notebook.graphs.ask import graph as ask_graph
from pages.components.model_selector import model_selector
from pages.stream_app.utils import convert_source_references, setup_page

setup_page("📝 Study Plan", sidebar_state="collapsed")

st.title("📝 Study Plan")
st.markdown("---")

# Add your tutor page content here
st.write("Ask your questions and get help from our AI tutor!")

study_plan_tab, search_tab = st.tabs(["Generate Study Plan", "Tutor"])

if "search_results" not in st.session_state:
    st.session_state["search_results"] = []

if "ask_results" not in st.session_state:
    st.session_state["ask_results"] = {}


async def process_ask_query(question, strategy_model, answer_model, final_answer_model):
    async for chunk in ask_graph.astream(
        input=dict(
            question=question,
        ),
        config=dict(
            configurable=dict(
                strategy_model=strategy_model.id,
                answer_model=answer_model.id,
                final_answer_model=final_answer_model.id,
            )
        ),
        stream_mode="updates",
    ):
        yield (chunk)


def results_card(item):
    score = item.get("relevance", item.get("similarity", item.get("score", 0)))
    with st.container(border=True):
        st.markdown(
            f"[{score:.2f}] **[{item['title']}](/?object_id={item['parent_id']})**"
        )
        if "matches" in item:
            with st.expander("Matches"):
                for match in item["matches"]:
                    st.markdown(match)


async def generate_detailed_content(week_content: str, model) -> str:
    async for chunk in ask_graph.astream(
        input=dict(
            question=f"Generate detailed content for this topic. Include examples and explanations: {week_content}",
            context=week_content
        ),
        config=dict(
            configurable=dict(
                model=model.id,
            )
        ),
        stream_mode="updates",
    ):
        if "write_final_answer" in chunk:
            return chunk["write_final_answer"]["final_answer"]
    return ""

async def generate_quiz(content: str, model) -> str:
    async for chunk in ask_graph.astream(
        input=dict(
            question="Generate 5 multiple choice questions to test understanding of this content",
            context=content
        ),
        config=dict(
            configurable=dict(
                model=model.id,
            )
        ),
        stream_mode="updates",
    ):
        if "write_final_answer" in chunk:
            return chunk["write_final_answer"]["final_answer"]
    return ""

async def process_study_plan(source: Source, placeholder):
    with placeholder.container():
        st.info("Generating study plan, please wait...")
    
    # Phase 1: Generate concise outline (one-liner per week)
    async for chunk in ask_graph.astream(
        input=dict(
            question="Break this content into a week-by-week study plan. For each week, provide ONLY a one-line topic summary. Format as 'Week 1: topic', 'Week 2: topic', etc.",
            context=source.full_text
        ),
        config=dict(
            configurable=dict(
                model=strategy_model.id,
            )
        ),
        stream_mode="updates",
    ):
        if "write_final_answer" in chunk:
            brief_plan = chunk["write_final_answer"]["final_answer"]
            source.add_insight("Study Plan Outline", brief_plan)
            
            # Split into weeks and process each
            weeks = brief_plan.split("Week")[1:]  # Skip empty first element
            total_weeks = len(weeks)
            
            progress_bar = placeholder.progress(0)
            for week_num, week_content in enumerate(weeks, 1):
                # Update progress
                progress = week_num / total_weeks
                progress_bar.progress(progress, f"Processing Week {week_num}/{total_weeks}")
                
                # Generate detailed content
                detailed_content = await generate_detailed_content(week_content, content_model)
                source.add_insight(f"Week {week_num} Content", detailed_content)
                
                # Generate quiz
                quiz_content = await generate_quiz(detailed_content, quiz_model)
                source.add_insight(f"Week {week_num} Quiz", quiz_content)
            
            progress_bar.empty()
            placeholder.success("Study plan generated! Switch to 'View Existing Plan' tab to see results.")

def display_study_plan(source: Source):
    insights = source.insights
    
    # Find and display outline
    outline = next((insight.content for insight in insights 
                   if insight.insight_type == "Study Plan Outline"), None)
    
    if outline:
        st.markdown("### Course Overview")
        st.markdown(outline)
        st.divider()
        
        # Display each week's content and quiz in expandable sections
        week_num = 1
        while True:
            content = next((insight.content for insight in insights 
                          if insight.insight_type == f"Week {week_num} Content"), None)
            quiz = next((insight.content for insight in insights 
                        if insight.insight_type == f"Week {week_num} Quiz"), None)
            
            if not content:
                break
                
            with st.expander(f"Week {week_num}", expanded=False):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown("#### 📚 Learning Content")
                    st.markdown(content)
                with col2:
                    st.markdown("#### ✍️ Practice Quiz")
                    st.markdown(quiz)
            
            week_num += 1





with study_plan_tab:
    st.title("Generate Study Plan")
    st.caption("Create a structured study plan from your document")
    
    # Source selection
    sources = Source.get_all()
    selected_source = st.selectbox(
        "Select a Source",
        options=sources,
        format_func=lambda x: x.title,
        key="source_selector"
    )
    
    if selected_source:
        # Model selection
        default_model = DefaultModels().default_chat_model
        strategy_model = model_selector(
            "Planning Model",
            "planning_model",
            selected_id=default_model,
            model_type="language",
            help="This model will create the initial study plan"
        )
        content_model = model_selector(
            "Content Generation Model",
            "content_model",
            model_type="language",
            selected_id=default_model,
            help="This model will generate detailed content for each week"
        )
        quiz_model = model_selector(
            "Quiz Generation Model",
            "quiz_model",
            model_type="language",
            selected_id=default_model,
            help="This model will generate quizzes for each week"
        )
        
        tab1, tab2 = st.tabs(["Generate New Plan", "View Existing Plan"])
        
        with tab1:
            if st.button("Generate Study Plan"):
                placeholder = st.empty()
                asyncio.run(process_study_plan(selected_source, placeholder))
                st.success("Study plan generated successfully!")
                st.rerun()
        
        with tab2:
            if selected_source:
                display_study_plan(selected_source)


    # st.subheader("Generate a Study Plan")
    # st.caption("Generate a structured study plan from your document")
    # default_model = DefaultModels().default_chat_model

    # sources = Source.get_all()  # Get all available sources
    # selected_source = st.selectbox(
    #     "Select a Source",
    #     options=sources,
    #     format_func=lambda x: x.title,
    #     key="source_selector"
    # )
    # if selected_source:
    #     st.session_state["source_id"] = selected_source.id


    # strategy_model = model_selector(
    #     "Planning Model",
    #     "planning_model",
    #     selected_id=default_model,
    #     model_type="language",
    #     help="This model will create the initial study plan"
    # )
    # content_model = model_selector(
    #     "Content Generation Model",
    #     "content_model",
    #     model_type="language",
    #     selected_id=default_model,
    #     help="This model will generate detailed content for each week"
    # )
    # quiz_model = model_selector(
    #     "Quiz Generation Model",
    #     "quiz_model",
    #     model_type="language",
    #     selected_id=default_model,
    #     help="This model will generate quizzes for each week"
    # )

    # async def process_study_plan(source_text):
    #     # Phase 1: Generate brief plan
    #     async for chunk in ask_graph.astream(
    #         input=dict(
    #             question="Create a week-by-week study plan from this content. Break it down into logical sections that can be studied sequentially.",
    #             context=source_text
    #         ),
    #         config=dict(
    #             configurable=dict(
    #                 model=strategy_model.id,
    #             )
    #         ),
    #         stream_mode="updates",
    #     ):
    #         if "write_final_answer" in chunk:
    #             brief_plan = chunk["write_final_answer"]["final_answer"]
    #             with placeholder.container(border=True):
    #                 st.subheader("Initial Study Plan")
    #                 st.markdown(brief_plan)

    #             # Phase 2: Generate detailed content
    #             async for content_chunk in ask_graph.astream(
    #                 input=dict(
    #                     question="For each week in this study plan, generate detailed content including examples and explanations",
    #                     context=brief_plan
    #                 ),
    #                 config=dict(
    #                     configurable=dict(
    #                         model=content_model.id,
    #                     )
    #                 ),
    #                 stream_mode="updates",
    #             ):
    #                 if "write_final_answer" in content_chunk:
    #                     detailed_content = content_chunk["write_final_answer"]["final_answer"]
    #                     with placeholder.container(border=True):
    #                         st.subheader("Detailed Weekly Content")
    #                         st.markdown(detailed_content)

    #                     # Phase 3: Generate quizzes
    #                     async for quiz_chunk in ask_graph.astream(
    #                         input=dict(
    #                             question="Generate 5 multiple choice questions for each week's content to test understanding",
    #                             context=detailed_content
    #                         ),
    #                         config=dict(
    #                             configurable=dict(
    #                                 model=quiz_model.id,
    #                             )
    #                         ),
    #                         stream_mode="updates",
    #                     ):
    #                         if "write_final_answer" in quiz_chunk:
    #                             quizzes = quiz_chunk["write_final_answer"]["final_answer"]
    #                             with placeholder.container(border=True):
    #                                 st.subheader("Weekly Quizzes")
    #                                 st.markdown(quizzes)

    # source = None
    # if "source_id" in st.session_state:
    #     source = Source.get(st.session_state["source_id"])

    # if source and source.full_text:
    #     placeholder = st.container()
    #     if st.button("Generate Study Plan"):
    #         asyncio.run(process_study_plan(source.full_text))
    # else:
    #     st.warning("Please select a source with content to generate a study plan")

with search_tab:
    with st.container(border=True):
        st.subheader("🔍 Search")
        st.caption("Search your knowledge base for specific keywords or concepts")
        search_term = st.text_input("Search", "")
        if not model_manager.embedding_model:
            st.warning(
                "You can't use vector search because you have no embedding model selected. Only text search will be available."
            )
            search_type = "Text Search"
        else:
            search_type = st.radio("Search Type", ["Text Search", "Vector Search"])
        search_sources = st.checkbox("Search Sources", value=True)
        search_notes = st.checkbox("Search Notes", value=True)
        if st.button("Search"):
            if search_type == "Text Search":
                st.write(f"Searching for {search_term}")
                st.session_state["search_results"] = text_search(
                    search_term, 100, search_sources, search_notes
                )
            elif search_type == "Vector Search":
                st.write(f"Searching for {search_term}")
                st.session_state["search_results"] = vector_search(
                    search_term, 100, search_sources, search_notes
                )
        for item in st.session_state["search_results"]:
            results_card(item)