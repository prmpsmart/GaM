
from ...thrift.regions.area import Area
from ...thrift.regions.client import Client
from ...thrift.regions.month import Month
from ...thrift.regions.year import Year
from ...thrift.regions.years import Years
from ..details.tdetails import TDetails
from .regionals import Regionals
from xml.etree.ElementTree import ElementTree as ET, ElementPath as EP, Element as E, SubElement as SE


class Xml:
    method = ["xml", "html", "text", "c14n"]
    subs = {"years": "years", "year": "months", "month": "areas", "area": "clients"}
    @classmethod
    def parse_region(cls, region=None, root=None, root_name=None):
        if root == None:
            if root_name == None: root_name = region.name
            root = E(root_name)
            top = root
        else:
            sub1 = SE(root, region.name)
            top = sub1
        dit = region.__dict__
        if region.which == "client":
            detts = Regionals.client_reg(region)
            dets = {"name":detts["name"], "details":detts["details"], "rate":detts["rate"]}
            for key, value in dets.items():
                if "_" in key: continue
                sub2 = SE(top, key)
                sub2.text = str(value)
        else:
            sub2 = top
            key = cls.subs[region.which]
            if region.which == "area":
                sub = SE(top, "details")
                dets = Regionals.details_str(region)
                sub.text = dets
                sub2 = SE(top, "clients")
            for sub_region in dit[key]: cls.parse_region(root=sub2, region=sub_region)
            
        return root
    @classmethod
    def parse_agam(cls, file):
        TDetails.update()
        root = cls.parse_region(region=Years, root_name="AGAM_Thrift")
        tree = ET(root)
        tree.write(file_or_filename=file, encoding=None, xml_declaration=1, method=cls.method[0])
    
    @classmethod
    def parse_xml(cls, file):
        tree = ET(file=file)
        root = tree.getroot()
        years = []
        for yr in root:
            # if yr.tag in Years.years_names: continue
            year = Year(yr.tag, 1)
            for mn in yr:
                month = Month(year, mn.tag, 1)
                for ar in mn:
                    area = Area(month, 1)
                    ar_dict = {}
                    for ar_tag in ar:
                        if ar_tag.tag == "clients":
                            for cl in ar_tag:
                                name = cl.tag
                                rate = int(cl.find("rate").text)
                                client = Client(area, name, rate, 1)
                                client.__dict__.update(Regionals.details_dict(cl.find("details").text))
                                client.update()
                        else: ar_dict.update(Regionals.details_dict(ar_tag.text))
                    area.__dict__.update(ar_dict)
            years.append(year)
        TDetails.update()
        return years


