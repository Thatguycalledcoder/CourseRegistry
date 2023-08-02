from processor import persist, ingest
import logging.config  # config file logging
from flask import Flask, request

# Setting basic configuration level for logging
# logging.basicConfig(level="INFO")  # Anything from info and above will work
# Sample log level messages
# logging.debug("This is a debug message")
# logging.info("This is an info message")
# logging.warning("This is an warning message")
# logging.error("This is an error message")
app = Flask(__name__)


@app.route('/get_courses', methods=['GET'])
def get_courses():
    db_object = persist.PersistData("postgres")
    courses = db_object.read_from_pg("futurexschema.futurex_course_catalog")
    return courses


@app.route('/add_course', methods=['POST'])
def add_course():
    input_json = request.get_json(force=True)
    print(input_json)
    db_object = persist.PersistData("postgres")
    db_object.write_from_json_to_pg("futurexschema.futurex_course_catalog", input_json)
    return "Success -- 200:\n" + str(input_json)


class DriverProgram:
    logging.config.fileConfig("./resources/configs/logging.conf")

    def __init__(self, filetype: str):
        print("Driver constructor initialized")
        self.filetype = filetype

    def my_function(self):
        print(f"Processing {self.filetype} file.")
        reader = ingest.FileReader(self.filetype)
        writer = persist.PersistData("Postgres")

        read_json = reader.read_file()
        print(f"Read json: {read_json}")
        writer.store_data(read_json)


if __name__ == "__main__":
    app.run(port=8005, debug=True)
    # driver = DriverProgram("json")
    #
    # driver.my_function()
