<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                              xmlns:cli="http://alexis.royer.free.fr/CLI"
                              xmlns:exsl="http://exslt.org/common" extension-element-prefixes="exsl">
<xsl:output method="text" encoding="iso-8859-1"/>

<xsl:include href="../../../../../../doc/licence/aggInsertLicence.xsl"/>
<xsl:include href="../../../../AggloToolKit/xsl/src/atkLayout.xsl"/>

<xsl:variable name="gsMenuName"><xsl:text>MENUNAME_</xsl:text></xsl:variable>
<xsl:variable name="gsMenuPrompt"><xsl:text>MENUPROMPT_</xsl:text></xsl:variable>
<xsl:variable name="gsMenuPath"><xsl:text>MENUPATH_</xsl:text></xsl:variable>



<xsl:template match="/cli:cli">

    <xsl:call-template name="insertCopyRight">
        <xsl:with-param name="aeTypeTarget" select="$gePython"/>
    </xsl:call-template>

    <xsl:value-of select="$gsEndl"/>
    <xsl:text>from agglo_cc import AccMenuPath</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:text>from agglo_cc import AccMenu</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:text>from agglo_cc import AccCliClient</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:text>from agglo_cc.core.cli_client import WAIT_TIMEOUT_MS</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:text>from agglo_cc.core.command_results import *</xsl:text><xsl:value-of select="$gsEndl"/>

    <!-- create menu name and path constants -->
    <xsl:call-template name="createMenuConstants"/>
    
    <!-- create menus -->
    <xsl:call-template name="createMenu">
        <xsl:with-param name="ansMenu" select="."/>
        <xsl:with-param name="asIndent" select="''"/>
    </xsl:call-template>
    <xsl:value-of select="$gsEndl"/>

    <!-- create client -->
    <xsl:call-template name="createClient"/>
    
</xsl:template>


<xsl:template name="createMenuConstants">

     <!-- TODO les constantes devrait etre dans le corps de chaque menu, on ferai classe.CONSTANT_PROMPT... -->
    <xsl:variable name="sRootMenuNameConstant">
        <xsl:call-template name="getMenuConstant">
            <xsl:with-param name="ansMenu" select="/cli:cli"/>
            <xsl:with-param name="asPrefix" select="$gsMenuName"/>
        </xsl:call-template>
    </xsl:variable>

    <xsl:value-of select="$gsEndl"/><xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sRootMenuNameConstant"/><xsl:text> = "</xsl:text><xsl:value-of select="/cli:cli/@name"/><xsl:text>"</xsl:text><xsl:value-of select="$gsEndl"/>
    
    <xsl:call-template name="getMenuConstant">
        <xsl:with-param name="ansMenu" select="/cli:cli"/>
        <xsl:with-param name="asPrefix" select="$gsMenuPrompt"/>
    </xsl:call-template>
    <xsl:text> = </xsl:text><xsl:value-of select="$sRootMenuNameConstant"/><xsl:text> + ">"</xsl:text><xsl:value-of select="$gsEndl"/>
    
    <xsl:call-template name="getMenuConstant">
        <xsl:with-param name="ansMenu" select="/cli:cli"/>
        <xsl:with-param name="asPrefix" select="$gsMenuPath"/>
    </xsl:call-template>
    <xsl:text> = AccMenuPath(</xsl:text><xsl:value-of select="$sRootMenuNameConstant"/><xsl:text>)</xsl:text><xsl:value-of select="$gsEndl"/>
    
    <!-- TODO ajouter /cli:cli a l'iteration -->
    <xsl:for-each select="/cli:cli/cli:menu">
        <xsl:variable name="sSubMenuNameConstant">
            <xsl:call-template name="getMenuConstant">
                <xsl:with-param name="ansMenu" select="."/>
                <xsl:with-param name="asPrefix" select="$gsMenuName"/>
            </xsl:call-template>
        </xsl:variable>
        <xsl:variable name="sSubMenuName" select="./@name"/>
        
        <xsl:value-of select="$sSubMenuNameConstant"/><xsl:text> = "</xsl:text><xsl:value-of select="./@name"/><xsl:text>"</xsl:text><xsl:value-of select="$gsEndl"/>
        
        <xsl:call-template name="getMenuConstant">
            <xsl:with-param name="ansMenu" select="."/>
            <xsl:with-param name="asPrefix" select="$gsMenuPrompt"/>
        </xsl:call-template>
        <xsl:text> = </xsl:text><xsl:value-of select="$sSubMenuNameConstant"/><xsl:text> + ">"</xsl:text><xsl:value-of select="$gsEndl"/>
        
        <xsl:call-template name="getMenuConstant">
            <xsl:with-param name="ansMenu" select="."/>
            <xsl:with-param name="asPrefix" select="$gsMenuPath"/>
        </xsl:call-template>
        <xsl:text> = AccMenuPath(</xsl:text><xsl:value-of select="$sSubMenuNameConstant"/><xsl:text>, </xsl:text>
        <xsl:call-template name="getMenuConstant">
            <xsl:with-param name="ansMenu" select="//*[./cli:keyword//cli:endl/cli:menu/@ref=$sSubMenuName]"/>
            <xsl:with-param name="asPrefix" select="$gsMenuPath"/>
        </xsl:call-template>
        <xsl:text>)</xsl:text><xsl:value-of select="$gsEndl"/>
    </xsl:for-each>
    
</xsl:template>


<xsl:template name="createMenu">
    <xsl:param name="ansMenu"/>
    
    <xsl:variable name="sClassName">
        <xsl:call-template name="getClassName">
            <xsl:with-param name="ansMenu" select="$ansMenu"/>
        </xsl:call-template>
    </xsl:variable>

    <xsl:value-of select="$gsEndl"/><xsl:value-of select="$gsEndl"/><xsl:value-of select="$gsEndl"/>
    <xsl:text>class </xsl:text><xsl:value-of select="$sClassName"/><xsl:text>(AccMenu):</xsl:text><xsl:value-of select="$gsEndl"/>
    
    <xsl:call-template name="createMenuInit">
        <xsl:with-param name="ansMenu" select="$ansMenu"/>
    </xsl:call-template>

    <xsl:if test="not($ansMenu=/cli:cli)">
        <xsl:call-template name="createEnterMenuCommand">
            <xsl:with-param name="ansMenu" select="$ansMenu"/>
        </xsl:call-template>
    </xsl:if>

    <xsl:call-template name="createMenuCommands">
        <xsl:with-param name="ansMenu" select="$ansMenu"/>
    </xsl:call-template>

    <xsl:call-template name="createSubMenus">
        <xsl:with-param name="ansMenu" select="$ansMenu"/>
    </xsl:call-template>
    
</xsl:template>


<xsl:template name="createClient">
    
    <xsl:variable name="sRootMenuClassName">
        <xsl:call-template name="getClassName">
            <xsl:with-param name="ansMenu" select="/cli:cli"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="sCodeIndent">
        <xsl:call-template name="incIndent">
            <xsl:with-param name="asIndent" select="$STR_Indent"/>
        </xsl:call-template>
    </xsl:variable>
    
    <xsl:value-of select="$gsEndl"/><xsl:value-of select="$gsEndl"/><xsl:value-of select="$gsEndl"/>
    <xsl:text>class AccCliClient</xsl:text><xsl:value-of select="/cli:cli/@name"/><xsl:text>(AccCliClient):</xsl:text><xsl:value-of select="$gsEndl"/>

 <xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$STR_Indent"/><xsl:text>def __init__(self, io_device, name="cli", io_logs=None, io_hub=None):</xsl:text><xsl:value-of select="$gsEndl"/>
  <xsl:value-of select="$sCodeIndent"/><xsl:text>super(AccCliClient</xsl:text><xsl:value-of select="/cli:cli/@name"/>
  <xsl:text>, self).__init__(name, </xsl:text><xsl:value-of select="$sRootMenuClassName"/><xsl:text>(), io_device, io_logs, io_hub)</xsl:text><xsl:value-of select="$gsEndl"/>

    <xsl:call-template name="createClientCommands">
        <xsl:with-param name="ansMenu" select="/cli:cli"/>
    </xsl:call-template>
        
</xsl:template>


<xsl:template name="createMenuInit">
    <xsl:param name="ansMenu"/>

    <xsl:variable name="sCodeIndent">
        <xsl:call-template name="incIndent">
            <xsl:with-param name="asIndent" select="$STR_Indent"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="sMenuClassName">
        <xsl:call-template name="getClassName">
            <xsl:with-param name="ansMenu" select="$ansMenu"/>
        </xsl:call-template>
    </xsl:variable>

    <!-- Create __init__ method prototype -->
    <xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$STR_Indent"/><xsl:text>def __init__(self</xsl:text>
    <xsl:if test="not($ansMenu=/cli:cli)">
        <xsl:text>, parent_menu</xsl:text>
    </xsl:if>
    <xsl:text>):</xsl:text><xsl:value-of select="$gsEndl"/>

    <!-- Create parent constructor method call -->
    <xsl:value-of select="$sCodeIndent"/><xsl:text>super(</xsl:text><xsl:value-of select="$sMenuClassName"/><xsl:text>, self).__init__(</xsl:text>
    <xsl:call-template name="getMenuConstant">
        <xsl:with-param name="ansMenu" select="$ansMenu"/>
        <xsl:with-param name="asPrefix" select="$gsMenuName"/>
    </xsl:call-template>
    <xsl:if test="not($ansMenu=/cli:cli)">
        <xsl:text>, parent_menu</xsl:text>
    </xsl:if>
    <xsl:text>)</xsl:text>
    <xsl:value-of select="$gsEndl"/>
    
    <!-- Create child menu instanciation method call -->
    <xsl:for-each select="$ansMenu/cli:keyword//cli:endl/cli:menu[@ref]">
        <xsl:variable name="sSubMenuName" select="./@ref"/>
        <xsl:variable name="nsSubMenu" select="/cli:cli/cli:menu[@name=$sSubMenuName]"/>
        <xsl:variable name="sSubMenuClassName">
            <xsl:call-template name="getClassName">
                <xsl:with-param name="ansMenu" select="$nsSubMenu"/>
            </xsl:call-template>
        </xsl:variable>
        <xsl:variable name="sMenuAttribute">
            <xsl:text>self.__</xsl:text>
            <xsl:call-template name="getMenuVariable">
                <xsl:with-param name="ansMenu" select="$nsSubMenu"/>
            </xsl:call-template>
        </xsl:variable>
        
        <xsl:value-of select="$sCodeIndent"/><xsl:value-of select="$sMenuAttribute"/><xsl:text> = </xsl:text>
        <xsl:value-of select="$sSubMenuClassName"/><xsl:text>(self)</xsl:text>
        <xsl:value-of select="$gsEndl"/>
        
    </xsl:for-each>
    
</xsl:template>


<xsl:template name="createEnterMenuCommand">
    <xsl:param name="ansMenu"/>

    <xsl:variable name="sCodeIndent">
        <xsl:call-template name="incIndent">
            <xsl:with-param name="asIndent" select="$STR_Indent"/>
        </xsl:call-template>
    </xsl:variable>

    <!-- Create command method prototype -->
    <xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$STR_Indent"/><xsl:text>@staticmethod</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$STR_Indent"/><xsl:text>def get_enter_command():</xsl:text><xsl:value-of select="$gsEndl"/>
    
    <!-- Declare local variables -->
    <xsl:value-of select="$sCodeIndent"/><xsl:text>result = ""</xsl:text><xsl:value-of select="$gsEndl"/>

    <!-- For each command referencing $ansMenu -->
    <xsl:for-each select="//cli:keyword//cli:endl/cli:menu[@ref=$ansMenu/@name]">
        
        <!-- For each keyword of the current command -->
        <!-- TODO faire avec createCommandSetParam une methode commune pour construire le result -->
        <xsl:for-each select="ancestor::cli:keyword">
            <xsl:value-of select="$gsEndl"/>
            <xsl:value-of select="$sCodeIndent"/><xsl:text>result += "</xsl:text>
            <xsl:if test="position()>1">
                <xsl:text> </xsl:text>
            </xsl:if>
            <xsl:value-of select="./@string"/><xsl:text>"</xsl:text><xsl:value-of select="$gsEndl"/>
        </xsl:for-each>
    </xsl:for-each>
    <xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sCodeIndent"/><xsl:text>result += "\n"</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$gsEndl"/>
    
    <xsl:value-of select="$sCodeIndent"/><xsl:text>return (result)</xsl:text><xsl:value-of select="$gsEndl"/>
    
</xsl:template>


<xsl:template name="createMenuCommands">
    <xsl:param name="ansMenu"/>
    
    <!-- For each endl of the menu -->
    <xsl:for-each select="$ansMenu/*[name()='keyword' or name()='param']//cli:endl">
        <xsl:variable name="bIsCommandGenerationNeeded">
            <xsl:call-template name="isCommandGenerationNeeded">
                <xsl:with-param name="ansLevelEndl" select="."/>
            </xsl:call-template>    
        </xsl:variable>
            
        <xsl:if test="$bIsCommandGenerationNeeded='true'">
            <!-- Create command method -->
            <xsl:call-template name="createMenuCommand">
                <xsl:with-param name="ansFinalEndl" select="."/>
            </xsl:call-template>
        </xsl:if>
        
    </xsl:for-each>
    
</xsl:template>


<xsl:template name="createMenuCommand">
    <xsl:param name="ansFinalEndl"/>

    <!-- <xsl:message><xsl:value-of select="$gsEndl"/>creation command <xsl:value-of select="$ansFinalEndl/../@id"/> <xsl:value-of select="$ansFinalEndl/../@string"/></xsl:message> -->
    <xsl:variable name="sCommandName">
        <xsl:call-template name="getCommandName">
            <xsl:with-param name="ansFinalEndl" select="$ansFinalEndl"/>
            <xsl:with-param name="abClientCommand" select="'false'"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="bHasOptionalLevels">
        <xsl:call-template name="isLevelOptional">
            <xsl:with-param name="ansLevelEndl" select="$ansFinalEndl"/>
            <xsl:with-param name="ansFinalEndl" select="$ansFinalEndl"/>
        </xsl:call-template>    
    </xsl:variable>
    <xsl:variable name="sCodeIndent">
        <xsl:call-template name="incIndent">
            <xsl:with-param name="asIndent" select="$STR_Indent"/>
        </xsl:call-template>
    </xsl:variable>

    <!-- Create command method prototype -->
    <!-- TODO generer l'aide a partir du xml -->
    <!-- # TODO rendre getCommand statique (methode de classe) -->
    <xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$STR_Indent"/><xsl:text>def </xsl:text><xsl:value-of select="$sCommandName"/>
    <xsl:text>(self</xsl:text>
    <xsl:call-template name="createCommandParameters">
        <xsl:with-param name="ansFinalEndl" select="$ansFinalEndl"/>
        <xsl:with-param name="abIsPrototype" select="'true'"/>
    </xsl:call-template>
    <xsl:text>):</xsl:text><xsl:value-of select="$gsEndl"/>
    
    <!-- Declare local variables -->
    <xsl:value-of select="$sCodeIndent"/><xsl:text>result = ""</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:if test="$bHasOptionalLevels='true'">
        <xsl:value-of select="$sCodeIndent"/><xsl:text>set_level = True</xsl:text><xsl:value-of select="$gsEndl"/>
    </xsl:if>

    <!-- For each level of the command -->
    <xsl:for-each select="$ansFinalEndl/ancestor::*[(name()='keyword' or name()='param') and (./cli:endl)]/cli:endl">
        <xsl:variable name="bIsLevelOptional">
            <xsl:call-template name="isLevelOptional">
                <xsl:with-param name="ansLevelEndl" select="."/>
                <xsl:with-param name="ansFinalEndl" select="$ansFinalEndl"/>
            </xsl:call-template>    
        </xsl:variable>
        <!-- <xsl:message>is level optional <xsl:value-of select="../@id"/> <xsl:value-of select="../@string"/> for final <xsl:value-of select="$ansFinalEndl/../@id"/> <xsl:value-of select="$ansFinalEndl/../@string"/> <xsl:value-of select="$bIsLevelOptional"/></xsl:message> -->
    
        <xsl:call-template name="createCommandSetLevel">
            <xsl:with-param name="ansLevelEndl" select="."/>
            <xsl:with-param name="abIsLevelOptional" select="$bIsLevelOptional"/>
        </xsl:call-template>
    </xsl:for-each>
    
    <xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sCodeIndent"/><xsl:text>result += "\n"</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$gsEndl"/>
    
    <xsl:value-of select="$sCodeIndent"/><xsl:text>return (result)</xsl:text><xsl:value-of select="$gsEndl"/>
    
</xsl:template>


<xsl:template name="createCommandSetLevel">
    <xsl:param name="ansLevelEndl"/>
    <xsl:param name="abIsLevelOptional"/>
    
    <!-- <xsl:message>createCommandSetLevel <xsl:value-of select="$ansLevelEndl/../@id"/> <xsl:value-of select="$ansLevelEndl/../@string"/> <xsl:value-of select="$abIsLevelOptional"/></xsl:message> -->
    <xsl:variable name="sCodeIndent">
        <xsl:call-template name="incIndent">
            <xsl:with-param name="asIndent" select="$STR_Indent"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="sSetResCodeIndent">
        <xsl:choose>
            <xsl:when test="$abIsLevelOptional='true'">
                <xsl:call-template name="incIndent">
                    <xsl:with-param name="asIndent" select="$sCodeIndent"/>
                </xsl:call-template>
            </xsl:when>

            <xsl:otherwise>
                <xsl:value-of select="$sCodeIndent"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>
    <xsl:variable name="nsPreviousEndl" select="$ansLevelEndl/../ancestor::*[(name()='keyword' or name()='param') and (./cli:endl)][1]/cli:endl"/>
    <!-- <xsl:variable name="bIsFirstLevel">
        <xsl:choose>
            <xsl:when test="count($ansLevelEndl/../ancestor::*/cli:endl)=0">true</xsl:when>

            <xsl:otherwise>false</xsl:otherwise>
        </xsl:choose>
    </xsl:variable> -->
    
    <!-- Set level authorization code generation -->
    <!-- TODO generer l'aide a partir du xml -->
    <xsl:value-of select="$gsEndl"/>
    <xsl:if test="$abIsLevelOptional='true'">
        <!-- <xsl:message>check triggering param<xsl:value-of select="$ansLevelEndl/@name"/></xsl:message> -->
        <xsl:value-of select="$sCodeIndent"/><xsl:text>set_level = set_level and (</xsl:text>

        <!-- <xsl:for-each select="$ansLevelEndl/ancestor::cli:param[generate-id($ansLevelEndl)=generate-id(.//cli:endl)]"> -->
        <!-- For each param of the level -->
        <!-- TODO a verifier -->
        <!-- <xsl:for-each select="$ansLevelEndl/ancestor::cli:param[(count(./cli:endl)=0) or (count($ansLevelEndl|./cli:endl)=count(./cli:endl))]"> -->
        <xsl:for-each select="$ansLevelEndl/ancestor::cli:param[count(.//cli:endl)=count($ansLevelEndl/..//cli:endl)]">
            <xsl:if test="position()>1">
                <xsl:text> and </xsl:text>
            </xsl:if>
            <xsl:value-of select="./@id"/><xsl:text> is not None</xsl:text>
        </xsl:for-each>
        <xsl:text>)</xsl:text><xsl:value-of select="$gsEndl"/>
        
        <xsl:value-of select="$sCodeIndent"/><xsl:text>if set_level:</xsl:text>
        <xsl:value-of select="$gsEndl"/>
    </xsl:if>

    <!-- For each keyword/param of the level -->
    <!-- <xsl:for-each select="$ansLevelEndl/ancestor::*[(name()='keyword' or name()='param') and (generate-id($ansLevelEndl)=generate-id(.//cli:endl))]"> -->
    <!-- <xsl:for-each select="$ansLevelEndl/ancestor::*[(name()='keyword' or name()='param') and ((count(./cli:endl)=0) or (count($ansLevelEndl|./cli:endl)=count(./cli:endl)))]"> -->
    <!-- <xsl:for-each select="$ansLevelEndl/ancestor::*[(name()='keyword' or name()='param') and (count(.//cli:endl)=count($ansLevelEndl/..//cli:endl))]"> -->
    <xsl:for-each select="$ansLevelEndl/ancestor::*[(name()='keyword') or (name()='param')]">
        
        <xsl:variable name="nsCurrentPreviousEndl" select="./ancestor::*[(name()='keyword' or name()='param') and (./cli:endl)][1]/cli:endl"/>

        <!-- TODO creer une method belongsTopSameLevel(ns, nsEndl) -->
        <!-- If current keyword/param belongs to nsPreviousEndl level -->
        <xsl:if test="generate-id($nsCurrentPreviousEndl)=generate-id($nsPreviousEndl)">
    
            <!-- Set param/keyword code generation -->
            <xsl:choose>
                <!-- TODO moduler le code en fonction de si le parent est un keyword ou un param, pour setter tous les keyword successifs d'un coup -->
                <!-- TODO il faut ajouter un ' ' si ce n'est pas le 1er level -->
                <xsl:when test="name()='keyword'">
                    <xsl:value-of select="$sSetResCodeIndent"/><xsl:text>result += "</xsl:text>
                    <xsl:if test="count(./ancestor::cli:keyword)>0">
                    <!-- <xsl:if test="($bIsFirstLevel='false') or (position()>1)"> -->
                        <xsl:text> </xsl:text>
                    </xsl:if>
                    <xsl:value-of select="./@string"/><xsl:text>"</xsl:text><xsl:value-of select="$gsEndl"/>
                </xsl:when>

                <xsl:otherwise>
                    <xsl:value-of select="$sSetResCodeIndent"/><xsl:text>result += " " + str(</xsl:text>
                    <xsl:value-of select="./@id"/><xsl:text>)</xsl:text><xsl:value-of select="$gsEndl"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:for-each>
</xsl:template>


<xsl:template name="createSubMenus">
    <xsl:param name="ansMenu"/>
    
    <!-- For each submenu -->
    <xsl:for-each select="$ansMenu/cli:keyword//cli:endl/cli:menu[@ref]">
        <xsl:variable name="sSubMenuName" select="./@ref"/>
    
        <!-- Create the sub menu -->
        <xsl:call-template name="createMenu">
            <xsl:with-param name="ansMenu" select="/cli:cli/cli:menu[@name=$sSubMenuName]"/>
        </xsl:call-template>
        
    </xsl:for-each>
    
</xsl:template>


<xsl:template name="createCommandParameters">
    <xsl:param name="ansFinalEndl"/>
    <xsl:param name="abIsPrototype"/>

    <!-- TODO passer en mode recursif -->
    <xsl:choose>
        <!-- If parameters are created for a method call -->
        <xsl:when test="$abIsPrototype='false'">
            <!-- For each parameter of the command -->
            <xsl:for-each select="$ansFinalEndl/ancestor::cli:param">
                <xsl:if test="position() &gt; 1">
                    <xsl:text>, </xsl:text>
                </xsl:if>
                <xsl:value-of select="./@id"/>
            </xsl:for-each>
        </xsl:when>

        <!-- If parameters are created for a prototype -->
        <xsl:otherwise>
            <!-- For each level of the command -->
            <!-- <xsl:message>create parameters for <xsl:value-of select="$ansFinalEndl/@name"/></xsl:message> -->
            <xsl:for-each select="$ansFinalEndl|$ansFinalEndl/../ancestor::*[(name()='keyword' or name()='param') and (./cli:endl)]/cli:endl">
                <xsl:variable name="nsCurrentLevel" select="."/>
                <xsl:variable name="bIsLevelOptional">
                    <xsl:call-template name="isLevelOptional">
                        <xsl:with-param name="ansLevelEndl" select="$nsCurrentLevel"/>
                        <xsl:with-param name="ansFinalEndl" select="$ansFinalEndl"/>
                    </xsl:call-template>    
                </xsl:variable>
                
                <!-- For each param of the level -->
                <!-- <xsl:message>level <xsl:value-of select="./@name"/> is optional  <xsl:value-of select="$bIsLevelOptional"/></xsl:message> -->
                <!-- <xsl:for-each select="$nsCurrentLevel/ancestor::cli:param[generate-id($nsCurrentLevel)=generate-id(.//cli:endl)]"> -->
                <!-- TODO a verifier -->
                <xsl:for-each select="$nsCurrentLevel/ancestor::cli:param[(count(./cli:endl)=0) or (count($nsCurrentLevel|./cli:endl)=count(./cli:endl))]">
                    <xsl:text>, </xsl:text><xsl:value-of select="./@id"/>
                    <xsl:if test="$bIsLevelOptional='true'">
                        <xsl:text>=None</xsl:text>
                    </xsl:if>
                </xsl:for-each>

            </xsl:for-each>
        </xsl:otherwise>
        
    </xsl:choose>
    
</xsl:template>


<xsl:template name="createClientCommands">
    <xsl:param name="ansMenu"/>
    
    <!-- For each endl of the menu -->
    <xsl:for-each select="$ansMenu/*[name()='keyword' or name()='param']//cli:endl">
        <xsl:variable name="bIsCommandGenerationNeeded">
            <xsl:call-template name="isCommandGenerationNeeded">
                <xsl:with-param name="ansLevelEndl" select="."/>
            </xsl:call-template>    
        </xsl:variable>
    
        <xsl:if test="$bIsCommandGenerationNeeded='true'">
            <xsl:call-template name="createClientCommand">
                <!-- TODO  supprimer le passage de ansMenu en argument -->
                <xsl:with-param name="ansMenu" select="$ansMenu"/>
                <xsl:with-param name="ansFinalEndl" select="."/>
            </xsl:call-template>
        </xsl:if>
        
    </xsl:for-each>

    <!-- For each submenu of the menu -->
    <xsl:for-each select="$ansMenu/cli:keyword//cli:endl/cli:menu[@ref]">
        <xsl:variable name="sSubMenuName" select="./@ref"/>
    
        <!-- Create the sub menu client commands -->
        <xsl:call-template name="createClientCommands">
            <xsl:with-param name="ansMenu" select="/cli:cli/cli:menu[@name=$sSubMenuName]"/>
        </xsl:call-template>
        
    </xsl:for-each>
    
</xsl:template>


<xsl:template name="createClientCommand">
    <xsl:param name="ansMenu"/>
    <xsl:param name="ansFinalEndl"/>

    <xsl:variable name="sMethodName">
        <xsl:call-template name="getCommandName">
            <xsl:with-param name="ansFinalEndl" select="$ansFinalEndl"/>
            <xsl:with-param name="abClientCommand" select="'true'"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="sCommandDecl">
        <xsl:value-of select="$STR_Indent"/><xsl:text>def </xsl:text><xsl:value-of select="$sMethodName"/><xsl:text>(</xsl:text>
    </xsl:variable>
    <xsl:variable name="sAlignment" select="translate($sCommandDecl, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_(', '                                                                ')"/>
    <xsl:variable name="sMenuVariable">
        <xsl:call-template name="getMenuVariable">
            <xsl:with-param name="ansMenu" select="$ansMenu"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="sCodeIndent">
        <xsl:call-template name="incIndent">
            <xsl:with-param name="asIndent" select="$STR_Indent"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="sIfIndent">
        <xsl:call-template name="incIndent">
            <xsl:with-param name="asIndent" select="$sCodeIndent"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="sIfIfIndent">
        <xsl:call-template name="incIndent">
            <xsl:with-param name="asIndent" select="$sIfIndent"/>
        </xsl:call-template>
    </xsl:variable>

    <!-- TODO il faudrait plutot un attribut check_prompt (default False) pour checker au besoin. Ca retire un argument expected_prompt a la methode -->
    <!-- Create command method prototype -->
    <xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sCommandDecl"/><xsl:text>self</xsl:text>
    <xsl:call-template name="createCommandParameters">
        <xsl:with-param name="ansFinalEndl" select="$ansFinalEndl"/>
        <xsl:with-param name="abIsPrototype" select="'true'"/>
    </xsl:call-template>
    <xsl:text>, \</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sAlignment"/><xsl:text>expected_result=None, expected_prompt=None, \</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sAlignment"/><xsl:text>timeout_ms=WAIT_TIMEOUT_MS):</xsl:text><xsl:value-of select="$gsEndl"/>
    
    <!-- Declare local variables -->
    <xsl:value-of select="$sCodeIndent"/><xsl:text>command_results = AccCommandResults("Execute </xsl:text><xsl:value-of select="$sMethodName"/><xsl:text>")</xsl:text><xsl:value-of select="$gsEndl"/>

    <!-- Check cli connection is opened -->
    <xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sCodeIndent"/><xsl:text>if not self.opened:</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sIfIndent"/><xsl:text>command_results.result = COMMAND_ERROR_CONNECTION</xsl:text><xsl:value-of select="$gsEndl"/>

    <!-- Navigation to menu code generation -->
    <!-- TODO verifier que le menu recupere est du bon type -->
    <!-- TODO integrer le resultat de navigate aux selecteurs result -->
    <xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sCodeIndent"/><xsl:text>if command_results.succeeded:</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sIfIndent"/><xsl:text>navigate_results = self._menu_navigator.navigate_to_menu(</xsl:text>
    <xsl:call-template name="getMenuConstant">
        <xsl:with-param name="ansMenu" select="$ansMenu"/>
        <xsl:with-param name="asPrefix" select="$gsMenuPath"/>
    </xsl:call-template>    
    <xsl:text>)</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sIfIndent"/><xsl:text>if navigate_results.children:</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sIfIfIndent"/><xsl:text>command_results.append_child(navigate_results)</xsl:text><xsl:value-of select="$gsEndl"/>


    <!-- Command invocation code generation -->
    <xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sCodeIndent"/><xsl:text>if command_results.succeeded:</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sIfIndent"/><xsl:value-of select="$sMenuVariable"/><xsl:text> = self._menu_navigator.current_menu</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sIfIndent"/><xsl:text>command = </xsl:text><xsl:value-of select="$sMenuVariable"/><xsl:text>.</xsl:text>
    <xsl:call-template name="getCommandName">
        <xsl:with-param name="ansFinalEndl" select="$ansFinalEndl"/>
        <xsl:with-param name="abClientCommand" select="'false'"/>
    </xsl:call-template>
    <xsl:text>(</xsl:text>
    <xsl:call-template name="createCommandParameters">
        <xsl:with-param name="ansFinalEndl" select="$ansFinalEndl"/>
        <xsl:with-param name="abIsPrototype" select="'false'"/>
    </xsl:call-template>
    <xsl:text>)</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sIfIndent"/><xsl:text>acc_execute_res = self.executeCommand(command, expected_result, expected_prompt, timeout_ms)</xsl:text><xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sIfIndent"/><xsl:text>command_results.append_child(acc_execute_res)</xsl:text><xsl:value-of select="$gsEndl"/>
    
    <!-- Method return -->
    <xsl:value-of select="$gsEndl"/>
    <xsl:value-of select="$sCodeIndent"/><xsl:text>return command_results</xsl:text><xsl:value-of select="$gsEndl"/>
    
</xsl:template>


<xsl:template name="isCommandGenerationNeeded">
    <xsl:param name="ansLevelEndl"/>

    <xsl:choose>
        <!-- If the command is a menu navigation command -->
        <xsl:when test="$ansLevelEndl/cli:menu">
            <xsl:text>false</xsl:text>
        </xsl:when>

        <!-- If this endl is the last of the command -->
        <xsl:when test="count($ansLevelEndl/..//cli:endl)=1">
            <xsl:text>true</xsl:text>
        </xsl:when>

        <!-- If this endl has several param/keyword following -->
        <!-- TODO revoir l'algorithme de generation -->
        <!-- TODO checker cette ligne -->
        <!-- TODO faut il generer si nbparam=1 and nbkeyword=1 -->
        <!-- TODO gerer le cas des param/keyword sans endl en dessous (parm/keyword mort, sans effet sur la generation) -->
        <xsl:when test="count($ansLevelEndl/../*[name()='keyword' or name()='param']) &gt; 1">
        <!-- <xsl:when test="(count($ansLevelEndl/../cli:keyword)>1) or (count($ansLevelEndl/../cli:param)>1)"> -->
            <!-- <xsl:text>false</xsl:text> -->
            <xsl:text>true</xsl:text>
        </xsl:when>
        
        <!-- If the command has no optional argument -->
        <!-- TODO checker cette ligne -->
        <!-- <xsl:when test="count($ansLevelEndl/ancestor::cli:keyword[last()]//cli:cpp)=1">
            <xsl:text>true</xsl:text>
        </xsl:when> -->
        
        <xsl:otherwise>
            <xsl:variable name="bDoNextLevelHaveNoTriggeringParam">
                <xsl:call-template name="doNextLevelHaveNoTriggeringParam">
                    <xsl:with-param name="ansLevelEndl" select="$ansLevelEndl"/>
                </xsl:call-template>
            </xsl:variable>
            <xsl:choose>
                <!-- <xsl:when test="$bDoNextLevelHaveNoTriggeringParam='true' and (count($ansLevelEndl/../cli:param)=0)"> -->
                <xsl:when test="$bDoNextLevelHaveNoTriggeringParam='true'">
                    <xsl:text>true</xsl:text>
                </xsl:when>
                
                <xsl:otherwise>
                    <xsl:text>false</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:otherwise>
        
    </xsl:choose>
        
</xsl:template>


<xsl:template name="doNextLevelHaveNoTriggeringParam">
    <xsl:param name="ansLevelEndl"/>

    <xsl:variable name="lsNoTriggeringParam">
        <!-- Iterate on all level following immediatly ansLevelEndl-->
        <!-- TODO checker cette ligne -->
        <!-- <xsl:for-each select="$ansLevelEndl/../cli:keyword//cli:endl"> -->
    
        <!-- For each of the level immediatly following $ansLevelEndl -->
        <xsl:for-each select="$ansLevelEndl/../*[name()='keyword' or name()='param']//cli:endl[generate-id($ansLevelEndl)=generate-id(./ancestor::*/cli:endl)]">
            <xsl:variable name="nsFollowingEndl" select="."/>
            <xsl:variable name="lsTriggeringParams" select="$nsFollowingEndl/ancestor::cli:param[count($ansLevelEndl|.//cli:endl)!=count($ansLevelEndl)]"/>
            <!-- <xsl:variable name="lsTriggeringParams" select="$ansLevelEndl/ancestor::cli:param[generate-id($ansLevelEndl)=generate-id(.//cli:endl)]"/> -->
            
            <xsl:if test="not($lsTriggeringParams)"><xsl:value-of select="$nsFollowingEndl/../@string"/> has no triggering param<xsl:value-of select="$gsEndl"/></xsl:if>
        </xsl:for-each>
    </xsl:variable>
    <!-- <xsl:message><xsl:value-of select="$lsNoTriggeringParam"/></xsl:message> -->
    
    <xsl:choose>
        <!-- <xsl:when test="not($lsNoTriggeringParam)">true</xsl:when> -->
        <xsl:when test="$lsNoTriggeringParam=''">false</xsl:when>
        <xsl:otherwise>true</xsl:otherwise>
    </xsl:choose>
    
</xsl:template>
   
   
<xsl:template name="isLevelOptional">
    <xsl:param name="ansLevelEndl"/>
    <xsl:param name="ansFinalEndl"/>
    
    <xsl:variable name="nsPreviousEndl" select="$ansLevelEndl/../ancestor::*[(name()='keyword' or name()='param') and (./cli:endl)][1]/cli:endl"/>
    
    <!-- TODO revoir l'algorithme de generation -->
    <xsl:choose>
        <!-- If the level is the first possible endl of the command line, its parameters are not optional -->
        <xsl:when test="count($nsPreviousEndl)=0">false</xsl:when>
        
        <xsl:otherwise>
            <!-- <xsl:message>verification level <xsl:value-of select="$ansLevelEndl/@name"/> optionnel : previous <xsl:value-of select="$nsPreviousEndl/@name"/> last <xsl:value-of select="$ansFinalEndl/@name"/></xsl:message> -->
            
            <xsl:variable name="lsGeneratedLevels">
                <!-- TODO ajouter ansLevelEndl? -->
                <!-- TODO ressemble beaucoup au code de isLevelNameGenerationNeeded -->
                <!-- Iterate on all possible endl of the command line, up to (but not including) ansFinalEndl, which is the currently generated command -->
                <xsl:for-each select="$nsPreviousEndl|$ansLevelEndl/..//cli:endl">
                    <!-- <xsl:message>test generation level <xsl:value-of select="../@id"/> <xsl:value-of select="../@string"/></xsl:message> -->
                    <xsl:variable name="bIsDescendant">
                        <xsl:call-template name="isEndlDescendant">
                            <xsl:with-param name="ansParentEndl" select="."/>
                            <xsl:with-param name="ansDescendantEndl" select="$ansFinalEndl"/>
                            <xsl:with-param name="bOrSelf" select="'false'"/>
                        </xsl:call-template>
                    </xsl:variable>
                    
                    <!-- Check that current endl actually belongs to the list of  possible endl of the command line, up to (but not including) ansFinalEndl -->
                    <!-- <xsl:message>test <xsl:value-of select="./@name"/> is ancestor of  <xsl:value-of select="$ansFinalEndl/@name"/> <xsl:value-of select="$bIsDescendant"/></xsl:message> -->
                    <xsl:if test="(generate-id(.)=generate-id($nsPreviousEndl)) or ($bIsDescendant='true')">
                        <xsl:variable name="bIsCurrentLevelGenerated"> 
                            <xsl:call-template name="isCommandGenerationNeeded">
                                <xsl:with-param name="ansLevelEndl" select="."/>
                            </xsl:call-template>
                        </xsl:variable>
                        
                        <!-- Check if current endl is a generated endl -->
                        <xsl:if test="$bIsCurrentLevelGenerated='true'"><xsl:value-of select="../@id"/><xsl:value-of select="../@string"/> Generated<xsl:value-of select="$gsEndl"/></xsl:if>
                    </xsl:if>
                </xsl:for-each>
            </xsl:variable>
            <!-- <xsl:message>test generation level <xsl:value-of select="$ansLevelEndl/../@id"/> <xsl:value-of select="$ansLevelEndl/../@string"/> for final  <xsl:value-of select="$ansFinalEndl/../@id"/> <xsl:value-of select="$ansFinalEndl/../@string"/> <xsl:value-of select="$gsEndl"/><xsl:value-of select="$lsGeneratedLevels"/></xsl:message> -->
                
            <xsl:choose>
                <!-- If a following endl is generated, ansLevelEndl is mandatory
                     If previous endl is generated, ansLevelEndl is mandatory -->
                <xsl:when test="not($lsGeneratedLevels='')">false</xsl:when>
                
                <!-- Otherwise ansLevelEndl is optional -->
                <xsl:otherwise>true</xsl:otherwise>
            </xsl:choose>
        </xsl:otherwise>
    </xsl:choose>
    
</xsl:template>


<xsl:template name="getCommandName">
    <xsl:param name="ansFinalEndl"/>
    <xsl:param name="abClientCommand"/>
    
    <!-- TODO passer la destination (menu ou client) en param pour generer correctement les noms cpp/@name -->
    <xsl:variable name="sCommandName">
        <xsl:choose>
            <!-- If generated method name is specified -->
            <xsl:when test="$ansFinalEndl/@name">
                <!-- Use specified name -->
                <xsl:value-of select="$ansFinalEndl/@name"/>
            </xsl:when>
            
            <!-- Otherwise ansLevelEndl is optional -->
            <xsl:otherwise>
                <!-- Otherwise generate method name by using keyword/param name -->
                <xsl:call-template name="recursiveGetCommandName">
                    <xsl:with-param name="ansLevelEndl" select="$ansFinalEndl"/>
                    <xsl:with-param name="abForceGenerateCurrentLevel" select="'false'"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>

    <xsl:choose>
        <!-- If method name is for cli client class -->
        <xsl:when test="$abClientCommand='true'">
            <xsl:if test="not($ansFinalEndl/@name)">
                <xsl:variable name="sMenuName" select="$ansFinalEndl/ancestor::*[(name()='cli' or name()='menu')][1]/@name"/>
                
                <xsl:value-of select="$sMenuName"/><xsl:text>_</xsl:text>
            </xsl:if>
            <xsl:value-of select="$sCommandName"/>
        </xsl:when>
        
        <!-- Otherwise method name is for a cli menu class -->
        <xsl:otherwise>
            <xsl:text>getCommand</xsl:text>
            <xsl:call-template name="upperCase">
                <xsl:with-param name="asString" select="$sCommandName"/>
                <xsl:with-param name="aiNbChar" select='1'/>
            </xsl:call-template>    
        </xsl:otherwise>
    </xsl:choose>
    
</xsl:template>


<xsl:template name="recursiveGetCommandName">
    <xsl:param name="ansLevelEndl"/>
    <xsl:param name="abForceGenerateCurrentLevel"/>

    <xsl:variable name="nsPreviousEndl" select="$ansLevelEndl/../ancestor::*[(name()='keyword' or name()='param') and (./cli:endl)][1]/cli:endl"/>
    <xsl:variable name="lsTriggeringKeywords" select="$ansLevelEndl/ancestor::cli:keyword[((count(./cli:endl)=0) or (count($ansLevelEndl|./cli:endl)=count(./cli:endl)))]"/>
    <xsl:variable name="bGenerateCurrentLevelName">
        <xsl:choose>
        
            <!-- If the level name generation is forced (because a bottom level name has been generated as well) -->
            <xsl:when test="$abForceGenerateCurrentLevel='true'">
                <!-- Generate current level name only with keywords. If it doesn't contain any keyword, do not generate -->
                <xsl:choose>
                    <xsl:when test="count($lsTriggeringKeywords)=0">false</xsl:when>
                    <xsl:otherwise>true</xsl:otherwise>
                </xsl:choose>
            </xsl:when>
        
            <xsl:otherwise>
                <xsl:call-template name="isLevelNameGenerationNeeded">
                    <xsl:with-param name="ansLevelEndl" select="$ansLevelEndl"/>
                </xsl:call-template>    
            </xsl:otherwise>
            
        </xsl:choose>
    </xsl:variable>
    <xsl:variable name="bForceGenerateCurrentLevel">
        <xsl:choose>
        
            <!-- If the level name generation is forced (because a bottom level name has been generated as well) -->
            <xsl:when test="$abForceGenerateCurrentLevel='true'">true</xsl:when>
        
            <xsl:otherwise><xsl:value-of select="$bGenerateCurrentLevelName"/></xsl:otherwise>
        </xsl:choose>
    </xsl:variable>
    
    <xsl:if test="$nsPreviousEndl">
        <xsl:call-template name="recursiveGetCommandName">
            <xsl:with-param name="ansLevelEndl" select="$nsPreviousEndl"/>
            <xsl:with-param name="abForceGenerateCurrentLevel" select="$bForceGenerateCurrentLevel"/>
        </xsl:call-template>
    </xsl:if>
    
    <!-- <xsl:message>generation nom level <xsl:value-of select="$ansLevelEndl/@name"/> <xsl:value-of select="$bGenerateCurrentLevelName"/></xsl:message> -->
    <xsl:if test="$bGenerateCurrentLevelName='true'">
        <xsl:call-template name="getLevelCommandName">
            <xsl:with-param name="ansLevelEndl" select="$ansLevelEndl"/>
            <!-- TODO filtrer les params -->
            <!-- <xsl:with-param name="bUseParam" select="'false'"/> -->
        </xsl:call-template>
    </xsl:if>
    
</xsl:template>


<xsl:template name="getLevelCommandName">
    <xsl:param name="ansLevelEndl"/>
    <!-- <xsl:param name="bUseParam" select="'false'"/> -->
    
    <!-- TODO passer en mode recursif -->
    <!-- TODO gestion du bUseParam -->
    <!-- TODO on pourrait s'arreter de generer a partir du 1er param -->
    <!-- <xsl:variable name="lsTriggeringKeywordParams" select="$ansLevelEndl/ancestor::*[(name()='keyword' or name()='param') and (generate-id($ansLevelEndl)=generate-id(.//cli:endl))]"/> -->
    <!-- <xsl:variable name="lsTriggeringKeywordParams" select="$ansLevelEndl/ancestor::*[(name()='keyword' or name()='param') and ((count(./cli:endl)=0) or (generate-id($ansLevelEndl)=generate-id(./cli:endl)))]"/> -->
    <xsl:variable name="lsTriggeringKeywordParams" select="$ansLevelEndl/ancestor::*[(name()='keyword' or name()='param') and ((count(./cli:endl)=0) or (count($ansLevelEndl|./cli:endl)=count(./cli:endl)))]"/>
    
    <!-- <xsl:message> <xsl:value-of select="$ansLevelEndl/@test"/> <xsl:value-of select="count($lsTriggeringKeywordParams)"/></xsl:message> -->

    <!-- Iterate on all keyword/params triggered by ansLevelEndl -->
    <xsl:for-each select="$lsTriggeringKeywordParams">

        <!-- If current trigger is a keyword, or if no keyword is present in level -->
        <!-- <xsl:if test="name()='keyword' or $bUseParam='true'"> -->
        <xsl:if test="name()='keyword' or count($lsTriggeringKeywordParams[name()='keyword'])=0">

            <xsl:choose>
                <!-- If current lexem is a keyword -->
                <xsl:when test="name()='keyword'">
                    <xsl:call-template name="upperCase">
                        <xsl:with-param name="asString">
                            <xsl:value-of select="./@string"/>
                        </xsl:with-param>
                        <xsl:with-param name="aiNbChar" select='1'/>
                    </xsl:call-template>    
                 </xsl:when>
                 
                <!-- If current lexem is a param -->
                <xsl:otherwise>
                    <xsl:call-template name="upperCase">
                        <xsl:with-param name="asString">
                            <xsl:value-of select="./@id"/>
                        </xsl:with-param>
                        <xsl:with-param name="aiNbChar" select='1'/>
                    </xsl:call-template>    
                </xsl:otherwise>
            </xsl:choose>
            
        </xsl:if>
    
    </xsl:for-each>
    
</xsl:template>


<!-- TODO reporter dans recursivegetcommandname -->
<xsl:template name="isLevelNameGenerationNeeded">
    <xsl:param name="ansLevelEndl"/>

    <xsl:variable name="nsPreviousEndl" select="$ansLevelEndl/../ancestor::*[(name()='keyword' or name()='param') and (./cli:endl)][1]/cli:endl"/>
    
    <!-- TODO revoir l'algorithme de generation -->
    <xsl:choose>
    
        <!-- If ansLevelEndl is the first endl -->
        <xsl:when test="not($nsPreviousEndl)">true</xsl:when>
 
        <xsl:otherwise>
            
            <!-- Generate level name if previous endl is generated -->
            <!-- TODO cet algo marche car cet invocation n'est pas faite si le forceGenerate est positionne. Si le forceGenerate n'ets pas positionne,
            cela signifie que les sous niveaux n'ont pas genere de nom. Donc il faut absoluement generer le nom de ce level, car le level suivant a ete genere.
            Donc il faut ajouter un lexeme au nom de la methode du endl precedent -->
            <xsl:call-template name="isCommandGenerationNeeded">
                <xsl:with-param name="ansLevelEndl" select="$nsPreviousEndl"/>
            </xsl:call-template>    

            <!-- Check if previous endl or sibbling levels of ansLevelEndl are generated -->
            <!-- <xsl:variable name="uiNbSibblingEndlGeneratedCommand">
                <xsl:for-each select="$nsPreviousEndl|$nsPreviousEndl/../*[(name()='keyword') or (name()='param')]//cli:endl">
                    <xsl:variable name="bIsCommandGenerationNeeded">
                        <xsl:call-template name="isCommandGenerationNeeded">
                            <xsl:with-param name="ansLevelEndl" select="."/>
                        </xsl:call-template>    
                    </xsl:variable> -->
                
                    <!-- If current keyword/param belongs to the command line triggered by ansLevelEndl -->
                    <!-- <xsl:if test="$bIsCommandGenerationNeeded='true'">1</xsl:if>
                </xsl:for-each>    
            </xsl:variable> -->
     
            <!-- <xsl:message>isLevelNameGenerationNeeded <xsl:value-of select="$ansLevelEndl/../@id"/> <xsl:value-of select="$ansLevelEndl/../@string"/> <xsl:value-of select="$uiNbSibblingEndlGeneratedCommand"/></xsl:message> -->
            <!-- <xsl:choose> -->
                <!-- Generate if parent endl is generated or has several child endl generated -->
                <!-- <xsl:when test="number($uiNbSibblingEndlGeneratedCommand)>1">true</xsl:when>
                <xsl:otherwise>false</xsl:otherwise>
            </xsl:choose> -->
        </xsl:otherwise>
        
    </xsl:choose>

</xsl:template>


<xsl:template name="isEndlDescendant">
    <xsl:param name="ansParentEndl"/>
    <xsl:param name="ansDescendantEndl"/>
    <xsl:param name="bOrSelf"/>
    
    <!-- <xsl:variable name="nsDescendantEndl" select="$ansParentEndl/..//cli:endl[generate-id()=generate-id($ansDescendantEndl)]"/> -->
    
    <xsl:choose>
        <xsl:when test="generate-id($ansParentEndl)=generate-id($ansDescendantEndl)">
            <xsl:value-of select="$bOrSelf"/>
        </xsl:when>
        <xsl:when test="count($ansParentEndl/..//cli:endl[generate-id(.)=generate-id($ansDescendantEndl)])=1">true</xsl:when>
        <xsl:otherwise>false</xsl:otherwise>
    </xsl:choose>
    
</xsl:template>


<xsl:template name="getMenuConstant">
    <xsl:param name="ansMenu"/>
    <xsl:param name="asPrefix"/>
    
    <xsl:value-of select="$asPrefix"/>
    <xsl:choose>
        <xsl:when test="$ansMenu=/cli:cli">
            <xsl:text>ROOT</xsl:text>
        </xsl:when>
        
        <xsl:otherwise>
            <xsl:call-template name="upperCase">
                <xsl:with-param name="asString" select="$ansMenu/@name"/>
            </xsl:call-template>
        </xsl:otherwise>
    </xsl:choose>
    
</xsl:template>


<xsl:template name="getMenuVariable">
    <xsl:param name="ansMenu"/>
    
    <xsl:text>Menu</xsl:text>
    <xsl:call-template name="upperCase">
        <xsl:with-param name="asString" select="$ansMenu/@name"/>
        <xsl:with-param name="aiNbChar" select='1'/>
    </xsl:call-template>
    
</xsl:template>


<xsl:template name="getClassName">
    <xsl:param name="ansMenu"/>

    <xsl:text>Acc</xsl:text>
    <xsl:call-template name="getMenuVariable">
        <xsl:with-param name="ansMenu" select="$ansMenu"/>
    </xsl:call-template>
    
</xsl:template>


</xsl:stylesheet>