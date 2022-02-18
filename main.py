# imports
import pandas as pd
import matplotlib.pyplot as plt


def categorical_data():
    # Initial sorting of the dataframe
    pd.set_option('precision', 0)
    df = pd.read_csv("PropertyData.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['year'] = df['Date'].dt.year
    df = df.drop(['Date'], axis=1)
    df = df.rename(columns={'Region_Name': 'region'})
    df = df.sort_values(by=['region', 'propertyType', 'year'])
    df = df.reset_index(drop=True)
    df['averagePrice'] = df['averagePrice'] / 1000

    # Creating separate list for each collection of data points
    lnd_det = list(df.iloc[0:21, 2])
    lnd_flt = list(df.iloc[21:42, 2])
    lnd_s_det = list(df.iloc[42:63, 2])
    lnd_ter = list(df.iloc[63:84, 2])
    ncl_det = list(df.iloc[84:105, 2])
    ncl_flt = list(df.iloc[105:126, 2])
    ncl_s_det = list(df.iloc[126:147, 2])
    ncl_ter = list(df.iloc[147:168, 2])
    years = list(df.iloc[0:21, 3])
    x = 0
    for i in years:
        years[x] = int(i)
        x += 1

    # Producing graph visualisation
    ax1 = plt.subplot(2, 2, 1)
    ax1.plot(years, lnd_det, color='#7a0177', marker='.', markersize=7)
    ax1.plot(years, lnd_s_det, color='#c51b8a', marker='.', markersize=7)
    ax1.plot(years, lnd_flt, color='#fbb4b9', marker='.', markersize=7)
    ax1.plot(years, lnd_ter, color='#f768a1', marker='.', markersize=7)
    ax1.plot(years, ncl_det, color='#7a0177', linestyle='-.')
    ax1.plot(years, ncl_s_det, color='#c51b8a', linestyle='-.')
    ax1.plot(years, ncl_flt, color='#fbb4b9', linestyle='-.')
    ax1.plot(years, ncl_ter, color='#f768a1', linestyle='-.')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Sold Price (£1000\'s)')
    ax1.set_xticks([2001, 2006, 2011, 2016, 2021])
    ax1.set_yticks([0, 200, 400, 600, 800, 1000])
    legend_handles = [plt.Line2D([], [], color='#7a0177'), plt.Line2D([], [], color='#c51b8a'),
                      plt.Line2D([], [], color='#f768a1'), plt.Line2D([], [], color='#fbb4b9')]
    legend1 = ax1.legend(legend_handles, ['Detached', 'Semi-Detached', 'Terraced', 'Flat'],
                         loc=2, title='House Types')
    legend_elements = [plt.Line2D([0], [0], color='k', label='London', marker='.', markersize=7),
                       plt.Line2D([0], [0], color='k', linestyle='-.', label='Newcastle')]
    ax1.add_artist(legend1)
    ax1.legend(handles=legend_elements, title='Location', loc='upper center', bbox_to_anchor=(0.35, 1),
               handlelength=3)
    ax1.set_title('Average Sold Prices for houses by type \n in London and Newcastle upon Tyne from 2001 to 2021')


def numerical_data():
    # Initial sorting of the dataframe
    df = pd.read_csv("BroadbandData.csv")
    rl = pd.read_csv("RegressionLine.csv")
    pd.set_option('precision', 1)
    df = df.drop(['laua'], axis=1)
    df = df.drop(['medUpload'], axis=1)
    df = df.drop(['medDown'], axis=1)
    df = df.rename(columns={'laua_name': 'region'})
    df['region'] = df['region'].str.title()
    df['outlier'] = ((df['averageDown'] > 130) | (df['averageUpload'] > 65))
    df = df.reset_index(drop=True)

    # Separate outliers
    outlier_up = []
    outlier_down = []
    normal_up = []
    normal_down = []
    for index, row in df.iterrows():
        if row['outlier']:
            outlier_up.append(row['averageUpload'])
            outlier_down.append(row['averageDown'])
        else:
            normal_up.append(row['averageUpload'])
            normal_down.append(row['averageDown'])
    # Producing graph visualisation
    ax2 = plt.subplot(2, 2, 2)
    ax2.scatter(outlier_down, outlier_up, color='#c51b8a')
    ax2.scatter(normal_down, normal_up, color='#fa9fb5')
    ax2.annotate('York', (143.75, 91))
    ax2.annotate('Kingston\nupon Hull', (156, 11))
    ax2.set_xlabel('Download Speed (Mb/S)')
    ax2.set_ylabel('Upload Speed (Mb/S)')
    ax2.plot(rl['x_vals'], rl['y_vals'], '--', color='k')
    leg_patch = ax2.add_patch(plt.Rectangle((25, 3), 95, 66, linewidth=1, edgecolor='grey',
                                            facecolor='none', linestyle='--'))
    ax2.legend([leg_patch, plt.scatter([], [], color='#c51b8a'), plt.scatter([], [], color='#fa9fb5'),
                plt.Line2D([], [], color='k', linestyle='--')],
               ['Main Data', 'Outliers', 'Main Data Points', 'Regression Line'])
    cor_coefficient = str(round(df["averageDown"].corr(df["averageUpload"]), 3))
    ax2.set_title('Upload and Download speeds in all regions of the UK\nwith correlation coefficient ' + cor_coefficient + ' (3 s.f.)')


def time_series_data():
    # Initial sorting of the dataframe
    df = pd.read_csv("FTSEData.csv")
    pd.set_option('precision', 1)
    df = df.drop(['High'], axis=1)
    df = df.drop(['Low'], axis=1)
    df = df.drop(['Volume'], axis=1)
    df = df.drop(['Dividends'], axis=1)
    df = df.drop(['Stock Splits'], axis=1)
    df = df.drop(['SYMBOL'], axis=1)
    df = df.drop(['Open'], axis=1)
    df['date'] = pd.to_datetime(df['date'])
    df = df.reset_index(drop=True)

    # Producing graph visualisation
    ax3 = plt.subplot(2, 2, 3)
    ax3.plot_date(df['date'], df['Close'], '-', color='#f768a1')
    ax3.axhline(y=df['Close'].mean(), linestyle='--', color='k')
    sma = df['Close'].rolling(7).mean()
    std = df['Close'].rolling(7).std()
    boll_up = sma + std * 2.0  # Calculate top band
    boll_down = sma - std * 2.0  # Calculate bottom band
    ax3.plot(df['date'], boll_up, linestyle="dashed", color="#ae017e")
    ax3.plot(df['date'], boll_down, linestyle="dashed", color="#fbb4b9")
    ax3.set_ylim(3000)
    ax3.set_xlim(pd.to_datetime('2008-01-01'), pd.to_datetime('2009-12-30'))
    ax3.set_xticks([pd.to_datetime('2008-01-01'), pd.to_datetime('2008-07-01'),
                    pd.to_datetime('2009-01-01'), pd.to_datetime('2009-07-01'),
                    pd.to_datetime('2009-12-31')])
    ax3.set_xlabel('Date (year-month-day)')
    ax3.set_ylabel('Index value (£\'s)')
    ax3.tick_params(axis='x', labelrotation=30)
    ax3.legend(['Stock Value', 'Average Stock Value', 'Bollinger Upper Band', 'Bollinger Lower Band'])
    ax3.set_title('Index value of the FTSE stock in GBP from 2008-2009 with Bollinger Bands®')


def narrative():
    # Make a text box with the narrative
    ax4 = plt.subplot(2, 2, 4)
    narrative_file = open('Narrative.txt', 'r')
    narrative_text = narrative_file.read()
    ax4.text(0, 0, narrative_text, transform=ax4.transAxes, fontsize='small',
             bbox=dict(facecolor='none', edgecolor='grey'))
    ax4.axis('off')


# Creation of figure
fig = plt.figure(figsize=(16, 9), dpi=120, constrained_layout=True)
categorical_data()
numerical_data()
time_series_data()
narrative()
fig.set_constrained_layout_pads(w_pad=0.2, h_pad=0.1, hspace=0, wspace=0)
fig.savefig('CSC3833.png', dpi=120)
