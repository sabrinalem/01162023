from flask import Flask, Response, render_template
import datetime
import pygal

app = Flask("DivineTiming")

@app.route('/')
def index():
    """ render svg on html """
    return """
<html>
    <body>
        <figure>
        <embed type="image/svg+xml" src="/graph/" />
        </figure>
    </body>
</html>'
"""


@app.route('/graph/')
def graph():
    """ render svg graph """
    sabrina_start = datetime.datetime(year=2022, month=11, day=4)
    lane_start = datetime.datetime(year=2022, month=12, day=20)
    sabrina_cycle = 30
    lane_cylce = 23
    today = datetime.datetime.now()
    elapse_sabrina = today - sabrina_start
    elapse_lane = today - lane_start
    if elapse_sabrina.days > sabrina_cycle:
        elapse_sabrina = elapse_sabrina.days % sabrina_cycle
    else:
        elapse_lane = elapse_lane.days
    if elapse_lane.days > lane_cylce:
        elapse_sabrina = elapse_sabrina.days % sabrina_cycle
    else:
        elapse_lane = elapse_lane.days
    sabrina_countdown = sabrina_cycle - elapse_sabrina
    lane_countdown = lane_cylce - elapse_lane

    chart = pygal.SolidGauge(inner_radius=0.75, truncate_legend=40)
    chart.title = 'Divine Timing'
    chart.add('Lane: ' + str(lane_countdown) + ' day(s) left in cycle',
              [{'value': elapse_lane, 'max_value': lane_cylce}])
    chart.add('Sabrina: ' + str(sabrina_countdown) + ' day(s) left in cycle',
              [{'value': elapse_sabrina, 'max_value': sabrina_cycle}])
    return Response(response=chart.render(), content_type='image/svg+xml')



if __name__ == '__main__':
    app.run()
