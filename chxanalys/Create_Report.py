'''
Yugang Created at Aug 08, 2016, CHX-NSLS-II

Create a PDF file from XPCS data analysis results, which are generated by CHX data analysis pipeline

How to use: 
python Create_Report.py  full_file_path uid  output_dir (option)

An exmplae to use:
python Create_Report.py  /XF11ID/analysis/2016_2/yuzhang/Results/August/af8f66/ af8f66

python Create_Report.py  /XF11ID/analysis/2016_2/yuzhang/Results/August/af8f66/ af8f66  /XF11ID/analysis/2016_2/yuzhang/Results/August/af8f66/test/

'''


import h5py

from reportlab.pdfgen  import  canvas
from reportlab.lib.units import inch, cm , mm   
from reportlab.lib.colors import pink, green, brown, white, black, red, blue


from reportlab.lib.styles import getSampleStyleSheet
#from reportlab.platypus import Image, Paragraph, Table

from reportlab.lib.pagesizes import letter, A4
from chxanalys.chx_generic_functions import (pload_obj )


from PIL import Image
from time import time
from datetime import datetime

import sys,os

 
 

class create_pdf_report( object ):
    
    '''Aug 16, YG@CHX-NSLS-II 
       Create a pdf report by giving data_dir, uid, out_dir
       data_dir: the input data directory, including all necessary images
       the images names should be:
            meta_file = 'uid=%s-md'%uid
            avg_img_file = 'uid=%s--img-avg-.png'%uid   
            ROI_on_img_file = 'uid=%s--ROI-on-Image-.png'%uid
            qiq_file = 'uid=%s--Circular-Average-.png'%uid   
            ROI_on_Iq_file = 'uid=%s--ROI-on-Iq-.png'%uid  

            Iq_t_file = 'uid=%s--Iq-t-.png'%uid
            img_sum_t_file = 'uid=%s--img-sum-t.png'%uid
            wat_file= 'uid=%s--Waterfall-.png'%uid
            Mean_inten_t_file= 'uid=%s--Mean-intensity-of-each-ROI-.png'%uid

            g2_file = 'uid=%s--g2-.png'%uid
            g2_fit_file = 'uid=%s--g2--fit-.png'%uid
            q_rate_file = 'uid=--%s--Q-Rate--fit-.png'%uid    

            two_time_file = 'uid=%s--Two-time-.png'%uid
            two_g2_file = 'uid=%s--g2--two-g2-.png'%uid
            
      uid: the unique id
      out_dir: the output directory
      report_type: 
          'saxs':  report saxs results
          'gisaxs': report gisaxs results
          
      
      Output: 
          A PDF file with name as "XPCS Analysis Report for uid=%s"%uid in out_dir folder
    '''       
    
    def __init__( self, data_dir, uid, out_dir=None, filename=None, load=True, report_type='saxs' ):
        self.data_dir = data_dir
        self.uid = uid
        if out_dir is None:
            out_dir = data_dir 
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        self.out_dir=out_dir
        
        self.styles = getSampleStyleSheet()
        self.width, self.height = letter
        
        self.report_type = report_type
        dt =datetime.now()
        CurTime = '%02d/%02d/%s/-%02d/%02d/' % ( dt.month, dt.day, dt.year,dt.hour,dt.minute)
        self.CurTime = CurTime
        if filename is None:
            filename="XPCS_Analysis_Report_for_uid=%s.pdf"%uid
        filename=out_dir + filename
        c = canvas.Canvas( filename, pagesize=letter)
        self.filename= filename
        c.setTitle("XPCS Analysis Report for uid=%s"%uid)
        self.c = c
        if load:
            self.load_metadata()
        
    def load_metadata(self):
        uid=self.uid
        data_dir = self.data_dir
        
        #load metadata        
        meta_file = 'uid=%s-md'%uid
        md = pload_obj( data_dir + meta_file )         
        
        self.md = md        
        self.sub_title_num = 0
        
        '''global definition'''
        
        try:
            beg = md['beg']
            end=md['end']
            uid_ = uid + '--fra-%s-%s'%(beg, end)
        except:
            uid_ = uid
            

        self.avg_img_file = 'uid=%s--img-avg-.png'%uid   
        
        self.ROI_on_img_file = 'uid=%s--ROI-on-Image-.png'%uid
        
        self.qiq_file = 'uid=%s--Circular-Average-.png'%uid  
        self.qiq_fit_file = 'uid=%s--form_factor--fit-.png'%uid 
        self.qr_1d_file = 'uid=%s--qr_1d-.png'%uid

        
        if self.report_type =='saxs':
            self.ROI_on_Iq_file = 'uid=%s--ROI-on-Iq-.png'%uid 
        else:
            self.ROI_on_Iq_file = 'uid=%s--qr_1d--ROI-.png'%uid 
        
        self.Iq_t_file = 'uid=%s--Iq-t-.png'%uid
        self.img_sum_t_file = 'uid=%s--img-sum-t.png'%uid
        self.wat_file= 'uid=%s--Waterfall-.png'%uid
        self.Mean_inten_t_file= 'uid=%s--Mean-intensity-of-each-ROI-.png'%uid

        self.g2_file = 'uid=%s--g2-.png'%uid_
        self.g2_fit_file = 'uid=%s--g2--fit-.png'%uid_
        self.q_rate_file = 'uid=%s--Q-Rate--fit-.png'%uid_    

        self.two_time_file = 'uid=%s--Two-time-.png'%uid_
        self.two_g2_file = 'uid=%s--g2--two-g2-.png'%uid_
        self.four_time_file = 'uid=%s--g4-.png'%uid_
        
        self.xsvs_fit_file = 'uid=%s--xsvs-fit-.png'%uid_
        self.contrast_file = 'uid=%s--contrast-.png'%uid_
        
        self.flow_g2v = 'uid=%s_1a_mqv--g2-v_fit-.png'%uid_
        self.flow_g2p = 'uid=%s_1a_mqp--g2-p_fit-.png'%uid_
        
        self.flow_g2v_rate_fit = 'uid=%s_v_fit_rate--Q-Rate--fit-.png'%uid_
        self.flow_g2p_rate_fit = 'uid=%s_p_fit_rate--Q-Rate--fit-.png'%uid_ 
        
        #self.report_header(page=1, top=730, new_page=False)
        #self.report_meta(new_page=False)
        
        
        
    def report_header(self, page=1, new_page=False):
        '''create headers, including title/page number'''
        c= self.c
        CurTime = self.CurTime
        uid=self.uid
        
        c.setFillColor(black)
        c.setFont("Helvetica", 14)
        #add page number
        c.drawString(250, 10, "Page--%s--"%( page ) )  
        #add time stamp
        c.drawString(380, 10, "created at %s@CHX"%( CurTime ) ) 
        #add title
        #c.setFont("Helvetica", 22)
        title = "XPCS Analysis Report for uid=%s"%uid        
        c.setFont("Helvetica", 1000/( len(title) )   )        
        #c.drawString(180,760, "XPCS Report of uid=%s"%uid )  #add title
        c.drawString(50,760, "XPCS Analysis Report for uid=%s"%uid )  #add title
        #add a line under title
        c.setStrokeColor( red )
        c.setLineWidth(width=1.5) 
        c.line( 50, 750, 550, 750  )
        if new_page:
            c.showPage()
            c.save()

        
    def report_meta(self, top=740, new_page=False):
        '''create the meta data report,
        the meta data include:  
            uid
            Sample:
            Measurement
            Wavelength
            Detector-Sample Distance
            Beam Center
            Mask file
            Data dir
            Pipeline notebook        
        '''

        c=self.c        
        #load metadata
        md = self.md
        try:
            uid = md['uid']
        except:
            uid=self.uid
            
        #add sub-title, metadata
        c.setFont("Helvetica", 20)
        
        ds = 15
        self.sub_title_num += 1
        c.drawString(10, top, "%s. Metadata"%self.sub_title_num )  #add title

        top = top - 5
        c.setFont("Helvetica", 11)
        i=1
        c.drawString(30, top-ds*i, 'UID: %s'%uid )
        c.drawString(30, top-ds*2, 'Sample: %s'%md['sample'] )
        c.drawString(30, top-ds*3, 'Data Acquisition From: %s To: %s'%(md['start_time'], md['stop_time'] ))        
        c.drawString(30, top-ds*4, 'Measurement: %s'%md['Measurement'] )
        c.drawString(30, top-ds*5, 'Wavelength: %s A | Num of Image: %d | Exposure time: %s ms | Acquire period: %s ms'%( md['incident_wavelength'],  int(md['number of images']),round(float(md['exposure time'])*1000,4), round(float(md['frame_time'])*1000,4)     ) )
        
        # shutter mode, feedback on/off, 'human' time stamp       
        
        c.drawString(30, top-ds*6, 'Detector-Sample Distance: %s m| FeedBack Mode: x -> %s & y -> %s| Shutter Mode: %s'%(
                md['detector_distance'], md['feedback_x'], md['feedback_y'], md['shutter mode']  ) )
        
        if self.report_type == 'saxs':
            c.drawString(30, top-ds*7, 
                            'Beam Center: [%s, %s] (pixel)'%(md['beam_center_x'], md['beam_center_y']) )
        elif self.report_type == 'gisaxs':
            c.drawString(30, top-ds*7, 
                            'Incident Center: [%s, %s] (pixel)'%(md['beam_center_x'], md['beam_center_y']) )
            c.drawString(280, top-ds*7, '||' )       
            c.drawString(350, top-ds*7, 
                'Reflect Center: [%s, %s] (pixel)'%(md['refl_center_x'], md['refl_center_y']) )  
            
        
        c.drawString(30, top-ds*8, 'Mask file: %s'%md['mask_file'] )
        
        s=  'Data dir: %s'%self.data_dir     
        #c.setFont("Helvetica", 1000/( len(s ) )   )  
        #c.setFont("Helvetica", 12)
        if (12*len(s )) >1000:
            c.drawString(30, top-ds*9, s[:1000//12] )
            c.drawString(30 + len('Data dir:')*6, top-ds*10, s[1000//12:] )
            line = 10
        else:              
            c.drawString(30, top-ds*9, s)
            line = 9
        s = 'Pipeline notebook: %s'%md['NOTEBOOK_FULL_PATH']
        #c.setFont("Helvetica", 800/( len(s ) )   )   
        c.setFont("Helvetica", 12)
        
        line +=1
        if (12*len(s )) >1000:
            c.drawString(30, top-ds*line, s[:1000//12] )
            c.drawString(30+  len('Pipeline notebook:')*6, top-ds*(line+1), s[1000//12:] )
        else:              
            c.drawString(30, top-ds*line, s)

        
        if new_page:
            c.showPage()
            c.save()
        
    def report_static( self, top=560, new_page=False, iq_fit=False):
        '''create the static analysis report
           two images:
               average intensity image
               circular average
        
        '''
        #add sub-title, static images

        c= self.c
        c.setFont("Helvetica", 20)
        uid=self.uid
        
        ds =  220
        self.sub_title_num +=1
        c.drawString(10, top, "%s. Static Analysis"%self.sub_title_num )  #add title

        #add average image
        c.setFont("Helvetica", 14)
        imgf = self.avg_img_file  
        image = self.data_dir + imgf
        if os.path.exists(image):
            im = Image.open( image )
            ratio = float(im.size[1])/im.size[0]
            height=  180
            c.drawImage( image, 60, top - ds,  width= height/ratio,height=height,mask=None)

            c.setFont("Helvetica", 16)
            c.setFillColor( blue) 
            c.drawString( 90, top- 35,  'Average Intensity Image'    )

            c.setFont("Helvetica", 12)
            c.setFillColor(red) 
            c.drawString( 80, top- 230,  'filename: %s'%imgf    )

        #add q_Iq
        if self.report_type == 'saxs':
            imgf = self.qiq_file 
            if iq_fit:
                imgf = self.qiq_fit_file  
            label = 'Circular Average'  
            lab_pos = 390
            fn_pos = 320
        else:
            imgf = self.qr_1d_file
            label = 'Qr-1D'
            lab_pos = 420
            fn_pos = 350
            
        image = self.data_dir + imgf
        
        if os.path.exists(image):
            im = Image.open( image )
            ratio = float(im.size[1])/im.size[0]
            height= 180
            c.drawImage( image, 320, top - ds,  width= height/ratio,height=height,mask=None)

            c.setFont("Helvetica", 16)
            c.setFillColor( blue) 
            c.drawString( lab_pos, top- 35,  label   )

            c.setFont("Helvetica", 12)
            c.setFillColor(red) 
            c.drawString( fn_pos, top- 230,  'filename: %s'%imgf    )  
            
        if new_page:
            c.showPage()
            c.save()
            
           

    def report_ROI( self, top= 300, new_page=False):
        '''create the static analysis report
            two images:
               ROI on average intensity image
               ROI on circular average
        '''   
        uid=self.uid
        c= self.c
        #add sub-title, static images
        c.setFillColor(black)
        c.setFont("Helvetica", 20)        
        ds = 230
        self.sub_title_num +=1
        c.drawString(10, top, "%s. Define of ROI"%self.sub_title_num )  #add title
        #add ROI on image
        c.setFont("Helvetica", 14)
        imgf = self.ROI_on_img_file
        image = self.data_dir + imgf
        im = Image.open( image )
        ratio = float(im.size[1])/im.size[0]
        height= 240
        #c.drawInlineImage( image, 30, top - ds*1.1,  width= height/ratio,height=height)
        c.drawImage( image, 60, top - ds*1.15,  width= height/ratio,height=height,mask= 'auto')
        c.setFont("Helvetica", 16)
        c.setFillColor( blue) 
        c.drawString( 110, top- 35,  'ROI on Image'    )
        c.setFont("Helvetica", 12)
        c.setFillColor(red) 
        c.drawString( 60, top- 260,  'filename: %s'%imgf    )
        
        
        #add q_Iq
        imgf = self.ROI_on_Iq_file
        image = self.data_dir + imgf
        if os.path.exists(image):
            im = Image.open( image )
            ratio = float(im.size[1])/im.size[0]
            height= 180
            c.drawImage( image, 320, top - ds,  width= height/ratio,height=height,mask=None)

            c.setFont("Helvetica", 16)
            c.setFillColor( blue) 
            c.drawString( 420, top- 35,  'ROI on Iq'    )
            c.setFont("Helvetica", 12)
            c.setFillColor(red) 
            c.drawString( 350, top- 260,  'filename: %s'%imgf    )
        
        if new_page:
            c.showPage()
            c.save()


    def report_time_analysis( self, top= 720,new_page=False):
        '''create the time dependent analysis report
           four images:
               each image total intensity as a function of time
               iq~t
               waterfall
               mean intensity of each ROI as a function of time               
        '''   
        c= self.c
        uid=self.uid
        #add sub-title, Time-dependent plot
        c.setFont("Helvetica", 20)
        top1=top
        ds = 20
        self.sub_title_num +=1
        c.drawString(10, top, "%s. Time Dependent Plot"%self.sub_title_num )  #add title
        c.setFont("Helvetica", 14)
        
        
        top = top1 - 160
        #add img_sum_t
        if self.report_type == 'saxs':
            ipos = 80
        elif self.report_type == 'gisaxs':
            ipos = 200
        imgf = self.img_sum_t_file
        
        image = self.data_dir + imgf
        if os.path.exists(image):
            im = Image.open( image )
            ratio = float(im.size[1])/im.size[0]
            height= 140
            c.drawImage( image, ipos, top,  width= height/ratio,height=height,mask=None)

            c.setFont("Helvetica", 16)
            c.setFillColor( blue) 
            c.drawString( ipos + 60, top1 - 20 ,  'img sum ~ t'    )

            c.setFont("Helvetica", 12)
            c.setFillColor(red) 
            c.drawString( ipos, top- 5,  'filename: %s'%imgf    )


            #plot iq~t
            if self.report_type == 'saxs':

                imgf = self.Iq_t_file
                image = self.data_dir + imgf
                im = Image.open( image )
                ratio = float(im.size[1])/im.size[0]
                height= 140
                c.drawImage( image, 350, top,  width= height/ratio,height=height,mask=None)

                c.setFont("Helvetica", 16)
                c.setFillColor( blue) 
                c.drawString( 420, top1-20 ,  'iq ~ t'    )

                c.setFont("Helvetica", 12)
                c.setFillColor(red) 
                c.drawString( 360, top- 5,  'filename: %s'%imgf    )
            elif self.report_type == 'gisaxs':
                pass


        top = top1 - 340
        #add waterfall plot
        imgf = self.wat_file
        image = self.data_dir + imgf
        if os.path.exists(image):
            im = Image.open( image )
            ratio = float(im.size[1])/im.size[0]
        height= 160
        if os.path.exists(image):
            c.drawImage( image, 80, top,  width= height/ratio,height=height,mask=None)

        c.setFont("Helvetica", 16)
        c.setFillColor( blue) 
        c.drawString( 140, top + height,  'waterfall plot'    )

        c.setFont("Helvetica", 12)
        c.setFillColor(red) 
        if os.path.exists(image):
            c.drawString( 80, top- 5,  'filename: %s'%imgf    )


        #add mean-intensity of each roi
        imgf = self.Mean_inten_t_file
        image = self.data_dir + imgf
        if os.path.exists(image):
            im = Image.open( image )
            ratio = float(im.size[1])/im.size[0]
            height= 160
            c.drawImage( image, 360, top,  width= height/ratio,height=height,mask=None)

            c.setFont("Helvetica", 16)
            c.setFillColor( blue) 
            c.drawString( 330, top + height,  'Mean-intensity-of-each-ROI'    )

            c.setFont("Helvetica", 12)
            c.setFillColor(red) 
            c.drawString( 310, top- 5,  'filename: %s'%imgf    )
        
        if new_page:
            c.showPage()
            c.save()

    def report_one_time( self, top= 350, g2_fit_file=None, q_rate_file=None, new_page=False):
        '''create the one time correlation function report
           Two images:
               One Time Correlation Function with fit
               q-rate fit
        '''   
        c= self.c
        uid=self.uid
        #add sub-title, One Time Correlation Function
        c.setFillColor(black)
        c.setFont("Helvetica", 20)
        ds = 20
        self.sub_title_num +=1
        c.drawString(10, top, "%s. One Time Correlation Function"%self.sub_title_num  )  #add title
        c.setFont("Helvetica", 14)
        #add g2 plot
        top = top - 320
        if g2_fit_file is None:
            imgf = self.g2_fit_file
        else:
            imgf = g2_fit_file
        image = self.data_dir + imgf
        im = Image.open( image )
        ratio = float(im.size[1])/im.size[0]
        height= 300
        c.drawImage( image, 1, top,  width= height/ratio,height=height, mask= 'auto')
        #c.drawImage( image, 1, top,  width= height/ratio,height=height, mask= None )
        c.setFont("Helvetica", 16)
        c.setFillColor( blue) 
        c.drawString( 150, top + height ,  'g2 fit plot'    )

        c.setFont("Helvetica", 12)
        c.setFillColor(red) 
        c.drawString( 80, top- 0,  'filename: %s'%imgf    )

        #add g2 plot fit
        top = top + 70 #
        if q_rate_file is None:
            imgf = self.q_rate_file
        else:
            imgf =  q_rate_file
        image = self.data_dir + imgf
        if os.path.exists(image):
            im = Image.open( image )
        
            ratio = float(im.size[1])/im.size[0]
            height= 180
            c.drawImage( image, 350, top,  width= height/ratio,height=height,mask= 'auto')

            c.setFont("Helvetica", 16)
            c.setFillColor( blue) 
            c.drawString( 450, top + 230,  'q-rate fit  plot'    )
            c.setFont("Helvetica", 12)
            c.setFillColor(red) 
            c.drawString( 380, top- 5,  'filename: %s'%imgf    )
        
        if new_page:
            c.showPage()
            c.save()

            
            
    def report_mulit_one_time( self, top= 720,new_page=False):
        '''create the mulit one time correlation function report
           Two images:
               One Time Correlation Function with fit
               q-rate fit
        '''   
        c= self.c
        uid=self.uid
        #add sub-title, One Time Correlation Function
        c.setFillColor(black)
        c.setFont("Helvetica", 20)
        ds = 20
        self.sub_title_num +=1
        c.drawString(10, top, "%s. One Time Correlation Function"%self.sub_title_num  )  #add title
        c.setFont("Helvetica", 14)
        #add g2 plot
        top = top - 320

        imgf = self.g2_fit_file
        image = self.data_dir + imgf
        if not os.path.exists(image):
            image = self.data_dir + self.g2_file
        im = Image.open( image )
        ratio = float(im.size[1])/im.size[0]
        height= 300
        c.drawImage( image, 1, top,  width= height/ratio,height=height, mask= 'auto')
        #c.drawImage( image, 1, top,  width= height/ratio,height=height, mask= None )
        c.setFont("Helvetica", 16)
        c.setFillColor( blue) 
        c.drawString( 150, top + height ,  'g2 fit plot'    )

        c.setFont("Helvetica", 12)
        c.setFillColor(red) 
        c.drawString( 80, top- 0,  'filename: %s'%imgf    )

        #add g2 plot fit
        top = top + 70 #
        imgf = self.q_rate_file
        image = self.data_dir + imgf
        if  os.path.exists(image):
            im = Image.open( image )
            ratio = float(im.size[1])/im.size[0]
            height= 180
            c.drawImage( image, 350, top,  width= height/ratio,height=height,mask= 'auto')

            c.setFont("Helvetica", 16)
            c.setFillColor( blue) 
            c.drawString( 450, top + 230,  'q-rate fit  plot'    )
            c.setFont("Helvetica", 12)
            c.setFillColor(red) 
            c.drawString( 380, top- 5,  'filename: %s'%imgf    )
        
        if new_page:
            c.showPage()
            c.save()

            
            
    def report_two_time( self, top= 720, new_page=False):
        '''create the one time correlation function report
           Two images:
               Two Time Correlation Function
               two one-time correlatoin function from multi-one-time and from diagonal two-time
        '''   
        c= self.c
        uid=self.uid
        #add sub-title, Time-dependent plot
        c.setFont("Helvetica", 20)
        
        ds = 20
        self.sub_title_num +=1
        c.drawString(10, top, "%s. Two Time Correlation Fucntion"%self.sub_title_num )  #add title
        c.setFont("Helvetica", 14)
        
        top1=top
        top = top1 - 330
        #add q_Iq_t
        imgf = self.two_time_file
        image = self.data_dir + imgf
        im = Image.open( image )
        ratio = float(im.size[1])/im.size[0]
        height= 300
        c.drawImage( image, 80, top,  width= height/ratio,height=height,mask=None)

        c.setFont("Helvetica", 16)
        c.setFillColor( blue) 
        c.drawString( 180, top + 300 ,  'two time correlation fucntion'    )

        c.setFont("Helvetica", 12)
        c.setFillColor(red) 
        c.drawString( 180, top- 10,  'filename: %s'%imgf    )
        top = top - 340
        #add q_Iq_t
        imgf = self.two_g2_file
        image = self.data_dir + imgf
        im = Image.open( image )
        ratio = float(im.size[1])/im.size[0]
        height= 300
        c.drawImage( image, 100, top,  width= height/ratio,height=height,mask=None)

        c.setFont("Helvetica", 16)
        c.setFillColor( blue) 
        c.drawString( 210, top + 310,  'compared g2'    )

        c.setFont("Helvetica", 12)
        c.setFillColor(red) 
        c.drawString( 180, top- 10,  'filename: %s'%imgf    )

        if new_page:
            c.showPage()
            c.save()
            

    def report_four_time( self, top= 720, new_page=False):
        '''create the one time correlation function report
           Two images:
               Two Time Correlation Function
               two one-time correlatoin function from multi-one-time and from diagonal two-time
        '''   
        
        c= self.c
        uid=self.uid
        #add sub-title, Time-dependent plot
        c.setFont("Helvetica", 20)
        
        ds = 20
        self.sub_title_num +=1
        c.drawString(10, top, "%s. Four Time Correlation Fucntion"%self.sub_title_num )  #add title
        c.setFont("Helvetica", 14)
        
        top1=top
        top = top1 - 330
        #add q_Iq_t
        imgf = self.four_time_file
        image = self.data_dir + imgf
        im = Image.open( image )
        ratio = float(im.size[1])/im.size[0]
        height= 300
        c.drawImage( image, 80, top,  width= height/ratio,height=height,mask=None)

        c.setFont("Helvetica", 16)
        c.setFillColor( blue) 
        c.drawString( 180, top + 300 ,  'four time correlation fucntion'    )

        c.setFont("Helvetica", 12)
        c.setFillColor(red) 
        c.drawString( 180, top- 10,  'filename: %s'%imgf    )      
 

        if new_page:
            c.showPage()
            c.save()  

            
    def report_flow_pv_g2( self, top= 720, new_page=False):
        '''create the one time correlation function report
           Two images:
               Two Time Correlation Function
               two one-time correlatoin function from multi-one-time and from diagonal two-time
        '''   
        c= self.c
        uid=self.uid
        #add sub-title, Time-dependent plot
        c.setFont("Helvetica", 20)
        
        ds = 20
        self.sub_title_num +=1
        c.drawString(10, top, "%s. Flow Analysis"%self.sub_title_num )  #add title
        c.setFont("Helvetica", 14)
        
        top1=top
        top = top1 - 330
        #add xsvs fit       
        
        imgf = self.flow_g2v
        image = self.data_dir + imgf
        im = Image.open( image )
        ratio = float(im.size[1])/im.size[0]
        height= 300
        c.drawImage( image, 80, top,  width= height/ratio,height=height,mask=None)     

        c.setFont("Helvetica", 16)
        c.setFillColor( blue) 
        c.drawString( 210, top + 300 ,  'XPCS Vertical Flow'    )
        c.setFont("Helvetica", 12)
        c.setFillColor(red) 
        c.drawString( 180, top- 10,  'filename: %s'%imgf    )
        
        
        
        imgf = self.flow_g2v_rate_fit
        image = self.data_dir + imgf
        im = Image.open( image )
        ratio = float(im.size[1])/im.size[0]
        height= 200
        c.drawImage( image, 350, top+50,  width= height/ratio,height=height,mask=None)     
        c.setFont("Helvetica", 12)
        c.setFillColor(red) 
        c.drawString( 350, top- 10 +50,  'filename: %s'%imgf    )
        
        
        
        
        
        top = top - 340
        #add contrast fit
        imgf = self.flow_g2p
        image = self.data_dir + imgf
        im = Image.open( image )
        ratio = float(im.size[1])/im.size[0]
        height= 300
        c.drawImage( image, 80, top,  width= height/ratio,height=height,mask=None)

        c.setFont("Helvetica", 16)
        c.setFillColor( blue) 
        c.drawString( 210, top + 310, 'XPCS Parallel Flow'  )        
        c.setFont("Helvetica", 12)
        c.setFillColor(red) 
        c.drawString( 180, top- 10,  'filename: %s'%imgf    )
        
        

        
        imgf = self.flow_g2p_rate_fit
        image = self.data_dir + imgf
        im = Image.open( image )
        ratio = float(im.size[1])/im.size[0]
        height= 200
        c.drawImage( image, 350, top+50,  width= height/ratio,height=height,mask=None)     
        c.setFont("Helvetica", 12)
        c.setFillColor(red) 
        c.drawString( 350, top- 10+50,  'filename: %s'%imgf    )
        

        if new_page:
            c.showPage()
            c.save()   

        
        
        
    def report_xsvs( self, top= 720, new_page=False):
        '''create the one time correlation function report
           Two images:
               Two Time Correlation Function
               two one-time correlatoin function from multi-one-time and from diagonal two-time
        '''   
        c= self.c
        uid=self.uid
        #add sub-title, Time-dependent plot
        c.setFont("Helvetica", 20)
        
        ds = 20
        self.sub_title_num +=1
        c.drawString(10, top, "%s. Visibility Analysis"%self.sub_title_num )  #add title
        c.setFont("Helvetica", 14)
        
        top1=top
        top = top1 - 330
        #add xsvs fit        
        imgf = self.xsvs_fit_file
        image = self.data_dir + imgf
        im = Image.open( image )
        ratio = float(im.size[1])/im.size[0]
        height= 300
        c.drawImage( image, 100, top,  width= height/ratio,height=height,mask=None)       
        
        

        c.setFont("Helvetica", 16)
        c.setFillColor( blue) 
        c.drawString( 210, top + 300 ,  'XSVS_Fit_by_Negtive_Binomal Function'    )
        
        

        c.setFont("Helvetica", 12)
        c.setFillColor(red) 
        c.drawString( 180, top- 10,  'filename: %s'%imgf    )
        top = top - 340
        #add contrast fit
        imgf = self.contrast_file
        image = self.data_dir + imgf
        im = Image.open( image )
        ratio = float(im.size[1])/im.size[0]
        height= 300
        c.drawImage( image, 100, top,  width= height/ratio,height=height,mask=None)

        c.setFont("Helvetica", 16)
        c.setFillColor( blue) 
        c.drawString( 210, top + 310, 'contrast get from xsvs and xpcs'  )

         
        
        c.setFont("Helvetica", 12)
        c.setFillColor(red) 
        c.drawString( 180, top- 10,  'filename: %s'%imgf    )

        if new_page:
            c.showPage()
            c.save()
      

            

    def new_page(self):
        c=self.c
        c.showPage()
    
    def save_page(self):
        c=self.c
        c.save()
        
    def done(self):
        out_dir = self.out_dir
        uid=self.uid
        
        print()
        print('*'*40)
        print ('The pdf report is created with filename as: %s'%(self.filename ))
        print('*'*40)


            
            
def create_multi_pdf_reports_for_uids( uids, g2, data_dir, report_type='saxs', append_name='' ):
    ''' Aug 16, YG@CHX-NSLS-II 
        Create multi pdf reports for each uid in uids
        uids: a list of uids to be reported
        g2: a dictionary, {run_num: sub_num: g2_of_each_uid}   
        data_dir:
        Save pdf report in data dir
    '''
    for key in list( g2.keys()):    
        i=1
        for sub_key in list( g2[key].keys() ):
            uid_i = uids[key][sub_key]
            data_dir_ = os.path.join( data_dir, '%s/'%uid_i ) 
            if append_name!='':
                uid_name = uid_i + append_name
            else:
                uid_name = uid_i
            c= create_pdf_report(  data_dir_, uid_i,data_dir,
                            report_type=report_type, filename="XPCS_Analysis_Report_for_uid=%s.pdf"%uid_name )    
            #Page one: Meta-data/Iq-Q/ROI
            c.report_header(page=1)
            c.report_meta( top=730)
            #c.report_one_time( top= 500 )
            #c.new_page()
            if report_type =='flow':
                c.report_flow_pv_g2( top= 720)    
            c.save_page()
            c.done() 
            
         
            

            
def create_one_pdf_reports_for_uids( uids, g2, data_dir, filename='all_in_one', report_type='saxs' ):
    ''' Aug 16, YG@CHX-NSLS-II 
        Create one pdf reports for each uid in uids
        uids: a list of uids to be reported
        g2: a dictionary, {run_num: sub_num: g2_of_each_uid}   
        data_dir:
        Save pdf report in data dir
    '''
    c= create_pdf_report( data_dir, uid=filename, out_dir=data_dir, load=False, report_type= report_type)
    page=1

    for key in list( g2.keys()):    
        i=1
        for sub_key in list( g2[key].keys() ):
            uid_i = uids[key][sub_key]
            data_dir_ = os.path.join( data_dir, '%s/'%uid_i)  
            
            c.uid = uid_i
            c.data_dir = data_dir_
            c.load_metadata()         
            
            #Page one: Meta-data/Iq-Q/ROI
            c.report_header(page=page)
            c.report_meta( top=730)
            c.report_one_time( top= 500 )
            c.new_page()
            page += 1
    c.uid = filename        
    c.save_page()
    c.done() 
    
    
def save_res_h5( full_uid, data_dir, save_two_time=False ):
    '''
       YG. Nov 10, 2016 
       save the results to a h5 file
       will save meta data/avg_img/mask/roi (ring_mask or box_mask)/
       will aslo save multi-tau calculated one-time correlation function g2/taus
       will also save two-time derived one-time correlation function /g2b/taus2
       if save_two_time if True, will save two-time correaltion function
    '''
    with h5py.File(data_dir + '%s.h5'%full_uid, 'w') as hf:  
        #write meta data
        meta_data = hf.create_dataset("meta_data", (1,), dtype='i')
        for key in md.keys():        
            try:
                meta_data.attrs[key] = md[key]
            except:
                pass

        shapes = md['avg_img'].shape
        avg_h5 = hf.create_dataset("avg_img", data = md['avg_img']  )
        mask_h5 = hf.create_dataset("mask", data = md['mask']  )
        roi_h5 = hf.create_dataset("roi", data = md['ring_mask']  )

        g2_h5 = hf.create_dataset("g2", data = g2 )
        taus_h5 = hf.create_dataset("taus", data = taus )

        if save_two_time:
            g12b_h5 = hf.create_dataset("g12b", data = g12b )
        g2b_h5 = hf.create_dataset("g2b", data = g2b )
        taus2_h5 = hf.create_dataset("taus2", data = taus2 )

def printname(name):
    print (name)
#f.visit(printname)
def load_res_h5( full_uid, data_dir   ):
    '''YG. Nov 10, 2016 
       load results from a h5 file
       will load meta data/avg_img/mask/roi (ring_mask or box_mask)/
       will aslo load multi-tau calculated one-time correlation function g2/taus
       will also load two-time derived one-time correlation function /g2b/taus2
       if save_two_time if True, will load two-time correaltion function
    
    '''
    with h5py.File(data_dir + '%s.h5'%full_uid, 'r') as hf:        
        meta_data_h5 = hf.get( "meta_data"  )
        meta_data = {}
        for att in meta_data_h5.attrs:        
            meta_data[att] =  meta_data_h5.attrs[att]         
        avg_h5 = np.array( hf.get("avg_img" ) )        
        mask_h5 = np.array(hf.get("mask" ))
        roi_h5 =np.array( hf.get("roi"  ))
        g2_h5 = np.array( hf.get("g2"  ))
        taus_h5 = np.array( hf.get("taus"  ))
        g2b_h5 = np.array( hf.get("g2b"))
        taus2_h5 = np.array( hf.get("taus2"))
        if 'g12b' in hf:
            g12b_h5 =   np.array( hf.get("g12b"))
    
    if 'g12b' in hf:
        return meta_data, avg_h5, mask_h5,roi_h5, g2_h5, taus_h5, g2b_h5, taus2_h5, g12b    
    else:    
        return meta_data, avg_h5, mask_h5,roi_h5, g2_h5, taus_h5, g2b_h5, taus2_h5    




