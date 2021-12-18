import itertools
import json
import os
import re
from pathlib import Path

from littleutils import only

from core.checker import check_entry
from core.text import pages, get_predictions
from core.utils import highlighted_markdown, make_test_input_callback


def test_steps():
    transcript = []
    for page_index, page in enumerate(pages.values()):
        for step_index, step_name in enumerate(page.step_names[:-1]):
            step = page.get_step(step_name)

            for substep in [*step.messages, step]:
                program = substep.program
                is_message = substep in step.messages

                if "\n" in program:
                    code_source = step.expected_code_source or "editor"
                else:
                    code_source = "shell"

                entry = dict(
                    input=program,
                    source=code_source,
                    page_slug=page.slug,
                    step_name=step_name,
                )

                output_parts = []
                def output_callback(data):
                    output_parts.extend(data["parts"])

                response = check_entry(
                    entry,
                    input_callback=make_test_input_callback(step.stdin_input),
                    output_callback=output_callback,
                )
                response["output_parts"] = output_parts
                normalise_response(response, is_message, substep)

                transcript_item = dict(
                    program=program.splitlines(),
                    page=page.title,
                    step=step_name,
                    response=response,
                )
                transcript.append(transcript_item)

                if step.get_solution and not is_message:
                    get_solution = "".join(step.get_solution["tokens"])
                    assert "def solution(" not in get_solution
                    assert "returns_stdout" not in get_solution
                    assert get_solution.strip() in program
                    transcript_item["get_solution"] = get_solution.splitlines()
                    if step.parsons_solution:
                        is_function = transcript_item["get_solution"][0].startswith(
                            "def "
                        )
                        assert len(step.get_solution["lines"]) >= 4 + is_function

                assert response["passed"] == (not is_message)

    path = Path(__file__).parent / "test_transcript.json"
    if os.environ.get("FIX_TESTS", 0):
        dump = json.dumps(transcript, indent=4, sort_keys=True)
        path.write_text(dump)
    else:
        assert transcript == json.loads(path.read_text())


def normalise_output(s):
    s = re.sub(r" at 0x\w+>", " at 0xABC>", s)
    return s


def normalise_response(response, is_message, substep):
    response["result"] = response.pop("output_parts")
    for line in response["result"]:
        line["text"] = normalise_output(line["text"])
        if line.get("isTraceback"):
            line["text"] = line["text"].splitlines()
    response["result"] = [
        list(group)[0] if istb else
        {"text": "".join(p["text"] for p in group), "color": color}
        for (color, istb), group in itertools.groupby(response["result"], key=lambda p: (p["color"], p.get("isTraceback")))
    ]

    response.pop("birdseye_objects", None)
    response.pop("awaiting_input", None)
    response.pop("error", None)
    response.pop("output", None)

    response["prediction"] = get_predictions(substep)
    if not response["prediction"]["choices"]:
        del response["prediction"]

    if is_message:
        response["message"] = only(response.pop("messages"))
        assert response["message"] == highlighted_markdown(substep.text)
    else:
        assert response.pop("messages") == []
        response["message"] = ""
