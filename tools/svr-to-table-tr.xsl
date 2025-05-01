<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:cml="http://www.xml-cml.org/schema" xmlns:svrl="http://purl.oclc.org/dsdl/svrl"
xmlns="http://www.w3.org/1999/xhtml" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:gvr="http://validationreport.gazelle.ihe.net/" version="2.0">
  <xsl:param name="elapsedTime" />
  <xsl:param name="title" />
  <xsl:param name="nameFile" />
  <xsl:template match="/">
    <xsl:apply-templates />
  </xsl:template>
  
  
  <xsl:template match="gvr:validationReport ">
    

            <xsl:choose>
              <xsl:when test="@result='PASSED'">
                <tr>
                  <td style="vertical-align:top">
                    <xsl:value-of select="$nameFile" />
                  </td> 
                  <td style="vertical-align:top"> 
                    <xsl:value-of select="@result" />
                  </td>
                  <td style="vertical-align:top">
                    <xsl:value-of select="//gvr:counters/@numberOfErrors" />
                  </td>
                  <td style="vertical-align:top">
                    <xsl:value-of select="//gvr:counters/@numberOfWarnings" />
                  </td>
                  <td style="vertical-align:top">
                    <xsl:value-of select="$elapsedTime"/>
                  </td>	
                  <td style="vertical-align:top">
                    <xsl:value-of select="//gvr:counters/@numberOfConstraints"/>
                  </td>                  
                  <td style="vertical-align:top">
                    <xsl:value-of select="/gvr:validationReport/gvr:validationOverview/gvr:validationServiceName" />-
                    <xsl:value-of select="/gvr:validationReport/gvr:validationOverview/gvr:validatorID" />
                    <xsl:apply-templates />
                  </td>

                </tr>
              </xsl:when>
              <xsl:otherwise>
                <tr>
                  <td style="vertical-align:top">
                    <xsl:value-of select="$nameFile" />
                  </td> 
                  <td style="vertical-align:top">
                    <xsl:value-of select="@result" />
                  </td>
                  <td style="vertical-align:top">
                    <xsl:value-of select="//gvr:counters/@numberOfErrors" />
                  </td>
                  <td style="vertical-align:top">
                    <xsl:value-of select="//gvr:counters/@numberOfWarnings" />
                  </td>
                  <td style="vertical-align:top">
                    <xsl:value-of select="$elapsedTime"/>
                  </td>	
                  <td style="vertical-align:top">
                    <xsl:value-of select="//gvr:counters/@numberOfConstraints"/>
                  </td>                  
                  <td style="vertical-align:top">
                    <xsl:value-of select="/gvr:validationReport/gvr:validationOverview/gvr:validationServiceName" />-
                    <xsl:value-of select="/gvr:validationReport/gvr:validationOverview/gvr:validatorID" />
                    <xsl:apply-templates />
                  </td>

                </tr>
              </xsl:otherwise>
            </xsl:choose>  


  </xsl:template>
  
  <xsl:template match="gvr:subReport">
    <xsl:if test="count(./gvr:constraint) &gt; 0">


          <h4>
            Details   (
            <xsl:value-of select="@subReportResult" />)   
          </h4>	  
        <table class="">
          <xsl:apply-templates />
        </table>
 
    </xsl:if>    
  </xsl:template>
  
  
  
  <xsl:template match="gvr:constraint">
    <tr>
      <td>	 
        <xsl:value-of select="@severity" />
      </td>
      <td class=".small">
        <small>
          <xsl:value-of select="gvr:constraintDescription" />
          <br/>
          <xsl:value-of select="gvr:locationInValidatedObject" />
        </small>
      </td>
    </tr>
  </xsl:template>
  
  <xsl:template match="*">
    <!-- drop these -->
  </xsl:template>
  
  <xsl:template name="break">
    <xsl:param name="text" select="string(.)"/>
    <xsl:choose>
      <xsl:when test="contains($text, '&#xa;')">
        <xsl:value-of select="substring-before($text, '&#xa;')"/>
        <br/>
        <xsl:call-template name="break">
          <xsl:with-param 
            name="text" 
            select="substring-after($text, '&#xa;')"
            />
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$text"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>  
  
</xsl:stylesheet>
