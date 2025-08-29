from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            length = float(request.form.get('length', 0))
            width  = float(request.form.get('width', 0))
            height = float(request.form.get('height', 0))
            doors  = int(request.form.get('doors', 0))
            windows = int(request.form.get('windows', 0))
            door_area = float(request.form.get('door_area', 2.0))    # m² لكل باب افتراضي 2.0
            window_area = float(request.form.get('window_area', 1.5))# m² لكل شباك افتراضي 1.5
            coats = float(request.form.get('coats', 1))              # عدد طبقات الدهان
            paint_price = float(request.form.get('paint_price', 0))  # سعر الدهان لكل م² (أو لكل م² × طبقات حسب اختيارك)
            labour_price = float(request.form.get('labour_price', 0))# سعر العمل لكل م²

            # حساب المساحة
            wall_area = 2 * (length + width) * height
            openings = doors * door_area + windows * window_area
            net_area = max(0.0, wall_area - openings)
            paintable_area = net_area * coats

            paint_cost = paintable_area * paint_price
            labour_cost = net_area * labour_price
            total_cost = paint_cost + labour_cost

            result = {
                'wall_area': round(wall_area, 2),
                'openings': round(openings, 2),
                'net_area': round(net_area, 2),
                'paintable_area': round(paintable_area, 2),
                'paint_cost': round(paint_cost, 2),
                'labour_cost': round(labour_cost, 2),
                'total_cost': round(total_cost, 2),
                'coats': coats
            }
        except Exception as e:
            result = {'error': str(e)}
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
