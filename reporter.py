import os
import csv
import json


# ============================================================
# TERMINAL REPORT
# ============================================================

def display_results(results):

    print("\n")

    print("=" * 90)

    print(
        "                 AI RESUME SCREENING RESULTS"
    )

    print("=" * 90)


    for rank, result in enumerate(
        results,
        start=1
    ):

        print(
            "\n" + "-" * 90
        )

        print(
            f"Rank: {rank}"
        )

        print(
            f"Candidate: "
            f"{result['candidate']}"
        )

        print(
            f"Final Score: "
            f"{result['final_score']:.2f}%"
        )

        print(
            f"Decision: "
            f"{result['decision']}"
        )

        print(
            f"Skill Match: "
            f"{result['skill_score']:.2f}%"
        )

        print(
            f"Semantic Similarity: "
            f"{result['semantic_score']:.2f}%"
        )

        print(
            f"Education Score: "
            f"{result['education_score']:.2f}%"
        )

        print(
            f"Experience Score: "
            f"{result['experience_score']:.2f}%"
        )

        print(
            f"Experience: "
            f"{result['experience_years']} years"
        )


        print("\nRequired Skills Matched:")

        print(
            ", ".join(
                result["required_matched"]
            )
            or "None"
        )


        print("\nRequired Skills Missing:")

        print(
            ", ".join(
                result["required_missing"]
            )
            or "None"
        )


        print("\nPreferred Skills Matched:")

        print(
            ", ".join(
                result["preferred_matched"]
            )
            or "None"
        )


        print("\nPreferred Skills Missing:")

        print(
            ", ".join(
                result["preferred_missing"]
            )
            or "None"
        )


# ============================================================
# SAVE CSV
# ============================================================

def save_csv(
    results,
    output_folder
):

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    file_path = os.path.join(
        output_folder,
        "ranked_candidates.csv"
    )


    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)


        writer.writerow([

            "Rank",
            "Candidate",
            "Final Score",
            "Decision",
            "Skill Score",
            "Semantic Score",
            "Education Score",
            "Experience Score",
            "Experience Years",
            "Required Matched",
            "Required Missing",
            "Preferred Matched",
            "Preferred Missing"
        ])


        for rank, result in enumerate(
            results,
            start=1
        ):

            writer.writerow([

                rank,

                result["candidate"],

                result["final_score"],

                result["decision"],

                result["skill_score"],

                result["semantic_score"],

                result["education_score"],

                result["experience_score"],

                result["experience_years"],

                ", ".join(
                    result["required_matched"]
                ),

                ", ".join(
                    result["required_missing"]
                ),

                ", ".join(
                    result["preferred_matched"]
                ),

                ", ".join(
                    result["preferred_missing"]
                )
            ])


    return file_path


# ============================================================
# SAVE JSON
# ============================================================

def save_json(
    results,
    output_folder
):

    os.makedirs(
        output_folder,
        exist_ok=True
    )


    file_path = os.path.join(
        output_folder,
        "ranked_candidates.json"
    )


    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )


    return file_path