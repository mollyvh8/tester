from flask import Flask, request, jsonify
from selenium import webdriver
# ... other necessary imports

app = Flask(__name__)

@app.route('/scrape_jobs', methods=['GET'])
def scrape_jobs():
    job_title = request.args.get('title')
    job_location = request.args.get('location')
    # Call your scrape_indeed function here
    job_listings = scrape_indeed(job_title, job_location)
    return jsonify(job_listings)

if __name__ == '__main__':
    app.run(debug=True)
