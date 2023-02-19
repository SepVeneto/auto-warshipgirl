from pick import pick
import Auto

title = '请选择关卡'
options = ['8-5', '9-1']

stage = pick(options, title)

app = Auto.Auto(stage)
app.run()

