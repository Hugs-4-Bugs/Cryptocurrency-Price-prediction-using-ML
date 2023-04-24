from django.shortcuts import render
from .forms import PredictionForm
from .model.data_collector import *
from .model.model import *
import datetime
# from datetime import datetime




def predict(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            date_str = str(date)
            year, month, day = date_str.split('-')

            year = int(year)
            month = int(month)
            day = int(day)
            symbol = form.cleaned_data['coin']

            start_date = datetime.datetime(2016, 1, 1)
            end_date = datetime.datetime(year, month, day)
            start_timestamp = int(start_date.timestamp())
            end_timestamp = int(end_date.timestamp())

            # Retrieve historical data and preprocess it
            data = get_historical_data(symbol, start_timestamp, end_timestamp)
            data = preprocess_data(data)
            data = add_features(data)

            # Train machine learning models
            actual_prices, model_price, model_return, X_test, y_price_test, y_return_test = train_model(data)

            # Make predictions
            input_data = data.tail(1)
            input_data = input_data.drop(['Price', 'Return'], axis=1)
            predicted_price = model_price.predict(input_data)[0]
            actual_price = model_price.predict(X_test)[-1]
            predicted_return = model_return.predict(input_data)[0]
            print(actual_price)
            return render(request, 'predict.html',
                          {'form': form, 'actual_price': actual_price, 'predicted_price': predicted_price,
                           'predicted_return': predicted_return})
    else:
        form = PredictionForm()

    return render(request, 'predict.html', {'form': form})


def news(request):
    news_data = get_crypto_news()
    for article in news_data:
        published_on_timestamp = article['published_on']
        published_on = datetime.datetime.fromtimestamp(published_on_timestamp)
        article['published_on'] = published_on
    context = {'news_data': news_data}
    return render(request, 'news.html', context)



def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')
