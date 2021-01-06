from pathlib import Path
import subprocess

from learning.models import Submission,Score


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def check_extension(filename, ext):
    filename = filename[::-1]
    filename = filename[:filename.find('.')]
    filename = filename[::-1]
    return ext == filename


# C/C++ code compile
def compile_c_cpp_submission(submission, language):
    solution_url = f"{BASE_DIR}{submission.solution.url}"
    result = 'AC'

    command = 'g++'
    executable_file_loc = f"{BASE_DIR}/media/userfiles/todo_coder"

    """
    Create an executable file for the solution named todo_coder
    """
    try:
        subprocess.run(f'{command} -o {executable_file_loc} {solution_url}', check=True, shell=True)
    except (subprocess.CalledProcessError, Exception) as e:
        result = 'CE'

    """
    Check whether extension is matches for chosen language
    """

    if result == 'AC':
        for testcase in submission.problem.testcases.all():
            input_url = f"{BASE_DIR}{testcase.input.url}"
            output_url = f"{BASE_DIR}/media/userfiles/todo_coder_output.txt"

            try:
                """ 
                Running executable file for the given time limit and memory limit of the problem
                Reads input from input_url file path and writes back output of the executable file in 
                output_url file path
                """
                p = subprocess.run(
                    f'ulimit -t {submission.problem.time_limit}; '
                    f'ulimit -v {submission.problem.memory_limit*1024}; '
                    f'{BASE_DIR}/media/userfiles/todo_coder < {input_url} > {output_url}',
                    shell=True
                )
                """
                Return Code 0 means Executable file ran without any error
                Return Code 137 means it didn't completed execution in given time
                Return Code 139 means it took more memory than given memory
                Return Code 255 means Run Time Error was caused by the code
                """

                if not p.returncode:
                    """
                    Reads output for the testcase and matches it with user's output
                    """
                    with open(output_url, 'r', encoding='UTF-8') as f:
                        participant_output = f.read()
                        if participant_output != testcase.output_text:
                            result = 'WA'
                            break
                elif p.returncode == 137:
                    result = 'TLE'
                elif p.returncode == 139:
                    result = 'MLE'
                else:
                    result = 'RTE'
            except (FileNotFoundError, Exception):
                result = 'CE'
                break

    # Update submission status
    if result=='AC' and not Submission.objects.filter(user=submission.user,status='AC',problem = submission.problem).exists():
        score = Score.objects.get(learner = submission.user)
        score.score += 5
        score.save()
    Submission.objects.filter(id=submission.id).update(status=result)


# Execute submitted file
def compile_submission(submission):
    compile_c_cpp_submission(submission, "C++")

