from google import genai
import json
from dotenv import load_dotenv
import os
from schema import SCHEMA

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_project(
    project,
    hours_per_day,
    days_per_week
):
    
    prompt = f"""
You are a senior project architect.

Project Classification
- Choose exactly one project_type.
- Valid values: Software, AI, Mechanical, Civil, Electrical, Research, Other.
- If AI/ML is a core component, classify as AI.
- Otherwise classify according to the primary engineering discipline.

Analyze the project and produce a complete project assessment.

Output Requirements
- Return exactly one JSON object.
- Output must be parseable by json.loads().
- Do not return markdown.
- Do not include explanations outside JSON.
- No comments.
- No trailing commas.

Schema:

{SCHEMA}

Rules:

Complexity
- Complexity must be Low, Medium, or High.
- Complexity_reasons must contain at most 3 items.

Estimation
- Estimated_effort_hours represents total person-hours.
- Effort hours should assume experienced professionals.
- Recommended_team_size must be an integer.
- Estimation_certainty must be Low, Medium, or High.
- Base the certainty on how much information is available and how predictable the project domain is.

Assumptions
- Include at most 3 assumptions used for estimation.

Team Composition
- Recommended_team is REQUIRED.
- Recommended_team_size must equal the sum of all role counts.
- Recommended_team must contain the key roles required to execute the project.
- Use role names appropriate to the project domain.
- Keep the team structure realistic and concise.
- Avoid unnecessary duplicate or overlapping roles.
- Every role must contain:
  - role
  - count

Risks
- Include at most 5 risks.

Deliverables
- Core_deliverables must contain the key outputs expected from the project.

Project Phases
- Project_phases must break the project into logical phases.
- Each phase must contain estimated_hours.
- Total phase hours should approximately equal estimated_effort_hours.

Implementation Roadmap
- Implementation_roadmap must describe the recommended execution order.
- Include actionable steps.
- Implementation roadmap must be ordered chronologically.
- Each step should build upon previous steps.

Technology Stack
- Recommended_stack must be null for non-software projects.
- Recommend only technologies directly required for implementation.

Future Enhancements
- Include at most 5 future enhancements.

Required Fields
- All fields defined in the schema must be returned.
- Do not omit any field.
- Use null or [] when information is unavailable.

If project requirements are vague:
- Make reasonable assumptions.
- Record assumptions in assumptions field.
- Lower estimation_certainty accordingly.


Project:
{project}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

    except Exception as e:

        raise Exception(
            f"Gemini API Error: {e}"
        )
    
    
    try:

        data = json.loads(
            response.text
        )

    except json.JSONDecodeError:

        raise Exception(
            "Invalid JSON returned by Gemini"
        )

    effort_hours = data.get(
        "estimated_effort_hours",
        0
    )

    team_size = max(
        1,
        int(
            data.get(
                "recommended_team_size"
            ) or 1
        )
    )
    if hours_per_day <= 0:
        raise Exception(
            "Hours per week must be greater than zero."
        )
    if days_per_week <= 0:
        raise Exception(
            "Days per week must be greater than zero."
        )

    hours_per_week = (
        hours_per_day *
        days_per_week
    )


    weeks_single = (
        effort_hours /
        hours_per_week
    )

    months_single = (
        weeks_single / 4.33
    )

    weeks_team = (
        effort_hours /
        (
            hours_per_week *
            team_size
        )
    )

    months_team = (
        weeks_team / 4.33
    )


    return (
        data,
        months_single,
        months_team,
        hours_per_week
    )














