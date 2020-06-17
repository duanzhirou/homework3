#coding:gbk
"""
�ۺ���Ŀ:������ʷ���ݻ������༰����ӻ�
���ߣ�������
���ڣ�6��15��
"""

import csv
import math
import pygal
import pygal_maps_world  # ������Ҫʹ�õĿ�


def read_csv_as_nested_dict(filename, keyfield, separator, quote):  # ��ȡԭʼcsv�ļ������ݣ���ʽΪǶ���ֵ�
    """
    �������:
      filename:csv�ļ���
      keyfield:����
      separator:�ָ���
      quote:���÷�
    ���:
      ��ȡcsv�ļ����ݣ�����Ƕ���ֵ��ʽ����������ֵ�ļ���Ӧ����keyfiled���ڲ��ֵ��Ӧÿ���ڸ�������Ӧ�ľ���ֵ
    """
    result = {}
    with open(filename, newline="") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            result[rowid] = row

    return result


# pygal_countries = pygal.maps.world.COUNTRIES #��ȡpygal.maps.world�й��Ҵ�����Ϣ��Ϊ�ֵ��ʽ�������м�Ϊpygal�и������룬ֵΪ��Ӧ�ľ������(���齫����ʾ����Ļ���˽�����ʽ���������ݣ�
# print(pygal_countries)


def reconcile_countries_by_name(plot_countries, gdp_countries):  # ������������GDP���ݵĻ�ͼ����Ҵ����ֵ䣬�Լ�û������GDP���ݵĹ��Ҵ��뼯��
    """
    �������:
    plot_countries: ��ͼ����Ҵ������ݣ��ֵ��ʽ�����м�Ϊ��ͼ����Ҵ��룬ֵΪ��Ӧ�ľ������
    gdp_countries:���и������ݣ�Ƕ���ֵ��ʽ�������ⲿ�ֵ�ļ�Ϊ���й��Ҵ��룬ֵΪ�ù��������ļ��е������ݣ��ֵ��ʽ)
    �����
    ����Ԫ���ʽ������һ���ֵ��һ�����ϡ������ֵ�����Ϊ��������GDP���ݵĻ�ͼ�������Ϣ��),
    ��������Ϊ��������GDP���ݵĻ�ͼ����Ҵ���
    """
    
    plot_gdp_countries_yes={}        #������GDP���ݵĻ�ͼ�����,�����ֵ�  
    not_plot_gdp_countries=set()        #������GDP���ݵĻ�ͼ����ң����뼯��
    for m in gdp_countries.values():    #�ж�����GDP�Ƿ���GDP����       
        if any(list(m.values())[4:]):
            country=m['Country Name']      #����л�ͼ����ҵĴ��룬�����ֵ��м���            
            if country in plot_countries.values():
                key=list(plot_countries.keys())[(list(plot_countries.values()).index(country))]
                plot_gdp_countries_yes[key]=country       #��Ϊ��ͼ������Ҵ��룬ֵΪ��Ӧ�ľ������
        else:
            country=m['Country Name']
            if country in plot_countries.values():
                key=list(plot_countries.keys())[(list(plot_countries.values()).index(country))]
                not_plot_gdp_countries.add(key)          #û��GDP���ݣ����ڼ�����

    return tuple([plot_gdp_countries_yes, not_plot_gdp_countries])     #����Ԫ���ʽ������һ���ֵ��һ�����ϡ������ֵ�����Ϊ��������GDP���ݵĻ�ͼ�������Ϣ




def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    �������:
    gdpinfo: gdp��Ϣ
	plot_countries: ��ͼ����Ҵ������ݣ��ֵ��ʽ�����м�Ϊ��ͼ����Ҵ��룬ֵΪ��Ӧ�ľ������
	year: �������ֵ
    �����
    �������һ���ֵ�Ͷ������ϵ�Ԫ�����ݡ������ֵ�����Ϊ��ͼ������Ҵ��뼰��Ӧ����ĳ�������GDP��ֵ����Ϊ��ͼ���и����Ҵ��룬ֵΪ�ھ�����ݣ���year����ȷ��������Ӧ������GDP����ֵ��Ϊ
    ������ʾ���㣬GDP�����ת��Ϊ��10Ϊ�����Ķ�����ʽ����GDPԭʼֵΪ2500����ӦΪlog2500��ps:����math.log()���)
    2������һ��Ϊ������GDP��������ȫû�м�¼�Ļ�ͼ����Ҵ��룬��һ������Ϊֻ��û��ĳ�ض��꣨��year����ȷ��������GDP���ݵĻ�ͼ����Ҵ���
   """
   
    a=read_csv_as_nested_dict(gdpinfo['gdpfile'], gdpinfo['country_name'], gdpinfo['separator'],gdpinfo['quote'])
    country_gdp_in_a_year={}            #�ɻ�ͼ�Ĺ�������ȫ���ɻ�ͼ�Ĺ��ң�plot_countries ��reconcile_countries_by_name()�����ķ���ֵ   
    plot_countries_yes,not_plot_countries=reconcile_countries_by_name(plot_countries,a)       #û��ĳ�ض�������GDP���ݵ����Ի�ͼ�Ļ�ͼ����Ҵ���
    plot_countries_no_gdp=set()     #����GDP��������ȫû�м�¼�Ļ�ͼ����Ҵ���
    all_countries_gdp={}
    for n in a.values():
        i=dict(zip(n.keys(), n.values()))
        all_countries_gdp[i['Country Name']]=i
    for code, country in plot_countries_yes.items():
        if country in all_countries_gdp.keys():
            year_gdp=all_countries_gdp[country][str(year)]
            if year_gdp:
                country_gdp_in_a_year[code]=math.log10(float(year_gdp))    #����math.log()��GDP���ת��Ϊ��10Ϊ�����Ķ�����ʽ
            else:
                plot_countries_no_gdp.add(code)

    return tuple([country_gdp_in_a_year, plot_countries_no_gdp, not_plot_countries])#�������һ���ֵ伴��ͼ������Ҵ��뼰��Ӧ����ĳ�������GDP��ֵ�Ͷ������ϼ�������GDP��������ȫû�м�¼�Ļ�ͼ����Ҵ��룬��һ������Ϊֻ��û��ĳ�ض��꣨��year����ȷ��������GDP���ݵĻ�ͼ����Ҵ����Ԫ������


def render_world_map(gdpinfo, plot_countries, year, map_file):  # ������ĳ�����������GDP����(����ȱ��GDP�����Լ�ֻ���ڸ���ȱ��GDP���ݵĹ���)�Ե�ͼ��ʽ���ӻ�
    """
    Inputs:
    gdpinfo:gdp��Ϣ�ֵ�
    plot_countires:��ͼ����Ҵ������ݣ��ֵ��ʽ�����м�Ϊ��ͼ����Ҵ��룬ֵΪ��Ӧ�ľ������
    year:����������ݣ����ַ�����ʽ������"1970"
    map_file:�����ͼƬ�ļ���
    Ŀ�꣺��ָ��ĳ����������GDP�����������ͼ����ʾ������������Ϊ����ĵ�ͼƬ�ļ�
    ��ʾ�����������ӻ���Ҫ����pygal.maps.world.World()����
    """
    world_map_chart=pygal.maps.world.World()
    plot_countries, plot_countries_no_gdp, not_plot_countries=build_map_dict_by_name(gdpinfo, plot_countries,year)
    world_map_chart.title='ȫ��GDP�ֲ�ͼ'              #���ݵĿ��ӻ����
    world_map_chart.add('%s'%year,plot_countries)
    world_map_chart.add('missing from world bank',plot_countries_no_gdp)
    world_map_chart.add('no data at this year',not_plot_countries)
    world_map_chart.render_to_file(map_file)

def test_render_world_map(year):  # ���Ժ���
    """
    �Ը����ܺ������в���
    """
    gdpinfo=dict(gdpfile="isp_gdp.csv", separator=",", quote='"', min_year=1960, max_year=2015,country_name="Country Name", country_code="Country Code")  # ���������ֵ�
    pygal_countries=pygal.maps.world.COUNTRIES            #��û�ͼ��pygal���Ҵ����ֵ�
    render_world_map(gdpinfo, pygal_countries, year, "isp_gdp_world_name_1981.svg") # ����ʱ����1970��Ϊ�����Ժ����������ԣ����Ը�����ݣ����ļ���������


# ������Ժ�����
print("��ӭʹ������GDP���ݿ��ӻ���ѯ")
print("----------------------")
year = input("���������ѯ�ľ������:")
test_render_world_map(year)
