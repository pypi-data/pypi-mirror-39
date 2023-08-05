#!/usr/bin/python
'''
Created on 13-Dec-2016

@author: vijay
'''
import wx
import os
from wx import TreeCtrl
from wx.lib.mixins.treemixin import ExpansionState
from src.view.constants import ID_newWorksheet, ID_CONNECT_DB, ID_deleteWithDatabase, \
    ID_DISCONNECT_DB, ID_ROOT_NEW_CONNECTION, ID_ROOT_REFERESH, keyMap, \
    ID_Import
# from src.view.table.CreateTable import CreateTableFrame
from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter, \
    ManageSqliteDatabase, SQLUtils
from src.view.connection.NewConnectionWizard import CreateNewConncetionWixard
from src.view.schema.CreateSchemaViewer import CreateErDiagramFrame
import logging
from src.view.table.CreateTable import CreatingTableFrame
from src.view.util.FileOperationsUtil import FileOperations
from src.view.importing.importCsvExcel import ImportingCsvExcelFrame
import ntpath
import datetime

logger = logging.getLogger('extensive')


class CreatingTreePanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        self.fileOperations = FileOperations()
        self.connDict = dict()
        vBox = wx.BoxSizer(wx.VERTICAL)
        ####################################################################
        self.sqlExecuter = SQLExecuter()
        self._treeList = self.sqlExecuter.getObject()
        self.treeMap = {}
        self.searchItems = {}
        self.tree = DatabaseNavigationTree(self)
        self.filter = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.filter.SetDescriptiveText("Type filter table name")
        self.filter.ShowCancelButton(True)
        self.filter.Bind(wx.EVT_TEXT, self.recreateTree)
        self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: self.filter.SetValue(''))
        self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
        self.recreateTree()
        
        # add drop target
        self.SetDropTarget(MyFileDropTarget(self))
#         self.tree.SetExpansionState(self.expansionState)
        self.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnTreeLeftDown)
        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.OnTreeDoubleclick)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onTreeItemActivated)
        self.tree.Bind(wx.EVT_TREE_KEY_DOWN, self.onTreeKeyDown)
        self.tree.Bind(wx.EVT_TREE_BEGIN_DRAG, self.onTreeBeginDrag)
        
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.OnTreeRightDown)
        self.tree.Bind(wx.EVT_RIGHT_UP, self.OnTreeRightUp)
#         self.tree.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown, self)
        ####################################################################
        vBox.Add(self.filter , 0, wx.EXPAND | wx.ALL)
        vBox.Add(self.tree , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)
        
    def OnSearch(self, event=None):

        value = self.filter.GetValue()
        if not value:
            self.recreateTree()
            return

        wx.BeginBusyCursor()
        try:
            for category, items in self._treeList[1]:
                self.searchItems[category] = []
                for childItem in items:
    #                 if SearchDemo(childItem, value):
                    self.searchItems[category].append(childItem)
        except Exception as e:
            logger.error(e, exc_info=True)
        wx.EndBusyCursor()
        self.recreateTree()   

    #---------------------------------------------    
    def recreateTree(self, evt=None):
        # Catch the search type (name or content)
#         searchMenu = self.filter.GetMenu().GetMenuItems()
#         fullSearch = searchMenu[1].IsChecked()
        fullSearch = False
            
        if evt:
            if fullSearch:
                # Do not`scan all the demo files for every char
                # the user input, use wx.EVT_TEXT_ENTER instead
                return
                    
        self.createDefaultNode()
                    
#         self.tree.Expand(self.root)
        
        self.tree.Thaw()
        self.searchItems = {}
    
    #---------------------------------------------
    def createDefaultNode(self):
        logger.debug("TreePanel.createDefaultNode")
        sqlExecuter = SQLExecuter()
        dbList = sqlExecuter.getListDatabase()

            
        fullSearch = False
        expansionState = self.tree.GetExpansionState()

        current = None
        item = self.tree.GetSelection()
        if item:
            prnt = self.tree.GetItemParent(item)
            if prnt:
                current = (self.tree.GetItemText(item), self.tree.GetItemText(prnt))
        self.tree.Freeze()
        self.tree.DeleteAllItems()
        self.root = self.tree.AddRoot("Connections")
        self.tree.SetItemImage(self.root, 0)
        data = dict()
        data['depth'] = 0
        self.tree.SetItemData(self.root, data)
        treeFont = self.tree.GetFont()
        catFont = self.tree.GetFont()

        # The native treectrl on MSW has a bug where it doesn't draw
        # all of the text for an item if the font is larger than the
        # default.  It seems to be clipping the item's label as if it
        # was the size of the same label in the default font.
        if 'wxMSW' not in wx.PlatformInfo:
            treeFont.SetPointSize(treeFont.GetPointSize() + 2)
            
        treeFont.SetWeight(wx.BOLD)
        catFont.SetWeight(wx.BOLD)
        self.tree.SetItemFont(self.root, treeFont)
        
        firstChild = None
        selectItem = None
        filter = self.filter.GetValue()
        count = 0
        for db in dbList:
            data = dict()
            data['depth'] = 1
            data['connection_name'] = db[1]
            data['db_file_path'] = db[2]
            if db[3] == 3:
                image = 17
            elif db[3] == 1:
                image = 16
#             elif db[3]==1:
#                 image=16
            
            # Appending connections
            item=self.addNode(targetNode=self.root, nodeLabel=db[1], pydata=data, image=image)
#             self.connDict[db[1]]['itemId']=item
            if db[1] in self.connDict.keys():
                self.getNodeOnOpenConnection(selectedItemId=item)
#         for key, value in self.connDict.items():
#             if value['isConnected']:
#                 logger.debug("{}:{}".format(key, value))
        self.tree.Expand(self.root)
        if firstChild:
            self.tree.Expand(firstChild)
#         if filter:
#             self.tree.ExpandAll()
        if expansionState:
            self.tree.SetExpansionState(expansionState)
        if selectItem:
            self.skipLoad = True
            self.tree.SelectItem(selectItem)
            self.skipLoad = False      
            
    def addNode(self, targetNode=None, nodeLabel='label', pydata=None, image=16):  
        nodeCreated = self.tree.AppendItem(targetNode, nodeLabel, image=image)
        self.tree.SetItemFont(nodeCreated, self.tree.GetFont())
        self.tree.SetItemData(nodeCreated, pydata)
        return nodeCreated     
    #---------------------------------------------
 
    #---------------------------------------------
    def OnItemExpanded(self, event):
        item = event.GetItem()
        logger.debug("OnItemExpanded: %s" % self.tree.GetItemText(item))
        event.Skip()

    #---------------------------------------------
    def OnItemCollapsed(self, event):
        item = event.GetItem()
#         logger.debug("OnItemCollapsed: %s" % self.tree.GetItemText(item))
        event.Skip()

    #---------------------------------------------
    def onTreeBeginDrag(self, event):
        logger.debug('onTreeBeginDrag')
        event.Skip()
        
    def onTreeItemActivated(self, event):
        logger.debug('onTreeItemActivated')
        self.onConnectDb(event)
        
    def onTreeKeyDown(self, event):
        logger.debug('onTreeKeyDown')
        keypress = self.GetKeyPress(event)
        keycode = event.GetKeyCode()
        keyname = keyMap.get(keycode, None)
        logger.debug('onTreeKeyDown keycode: %s  keyname:%s keypress: %s', keycode, keyname, keypress)
        logger.debug(keypress == 'WXK_F2')
        
        if keypress == 'Ctrl+C':
            self.onTreeCopy(event)
        elif keypress == 'WXK_F2':
            self.onF2KeyPress(event)
        elif keypress == 'WXK_DELETE':
            self.onDeleteKeyPress(event)
        event.Skip()
        
    def GetKeyPress(self, evt):
        keycode = evt.GetKeyCode()
        keyname = keyMap.get(keycode, None)
        modifiers = ""
        for mod, ch in ((evt.GetKeyEvent().ControlDown(), 'Ctrl+'),
                        (evt.GetKeyEvent().AltDown(), 'Alt+'),
                        (evt.GetKeyEvent().ShiftDown(), 'Shift+'),
                        (evt.GetKeyEvent().MetaDown(), 'Meta+')):
            if mod:
                modifiers += ch
    
        if keyname is None:
            if 27 < keycode < 256:
                keyname = chr(keycode)
            else:
                keyname = "(%s)unknown" % keycode
        return modifiers + keyname

    #----------------------------------------------------------------------
    def onDeleteKeyPress(self, event):
        try:
            logger.debug(self.tree.GetItemData(self.tree.GetSelection()))
            depth = self.tree.GetItemData(self.tree.GetSelection())['depth']
            if depth == 1:
                self.onDeleteConnection(event)
            elif depth == 3:
                logger.debug("TODO delete table")
                self.onDeleteTable(event)
            elif depth == 5:
                logger.debug("TODO delete column")
        except Exception as e:
            logger.error(e, exc_info=True)

    #----------------------------------------------------------------------
    def onF2KeyPress(self, event):
        try:
            logger.debug(self.tree.GetItemData(self.tree.GetSelection()))
            depth = self.tree.GetItemData(self.tree.GetSelection())['depth']
            if depth == 3:
                self.onRenameTable(event)
            elif depth == 5:
                self.onRenameColumn(event)
                
        except Exception as e:
            logger.error(e, exc_info=True)
    
    def onTreeCopy(self, event):
        """"""
        self.dataObj = wx.TextDataObject()
        self.dataObj.SetText(self.tree.GetItemText(self.tree.GetSelection()))
        if not wx.TheClipboard.IsOpened():  # may crash, otherwise
            wx.TheClipboard.Open()
        try:
            with wx.Clipboard.Get() as clipboard:
                clipboard.SetData(self.dataObj)
        except TypeError:
            wx.MessageBox("Unable to open the clipboard", "Error")
        
    def OnTreeDoubleclick(self, event):
        logger.info("OnTreeDoubleclick")
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        data = self.tree.GetItemData(item)
        rightClickDepth = data['depth']
        logger.info("Depth: {}".format(data['depth']))
        if rightClickDepth == 1:
            self.onConnectDb(event)
        if rightClickDepth == 3:
            # Open a new tab in SQL execution Pane. It is for table info.
            # TODO 
            sheetName = "tableInfo_{}".format(self.tree.GetItemText(item))
            self.openWorksheet(sheetName=sheetName)
        if self.tree.IsExpanded(item):
            self.tree.Collapse(item)
        else:
            self.tree.Expand(item)
        
    def OnTreeLeftDown(self, event):
        # reset the overview text if the tree item is clicked on again
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item and item == self.tree.GetSelection():
            logger.debug(self.tree.GetItemText(item) + " Overview")
        event.Skip()

    #---------------------------------------------
    def OnSelChanged(self, event):
        logger.debug('OnSelChanged')
        pass

    #---------------------------------------------
    def OnTreeRightDown(self, event):
        
        pt = event.GetPosition()
        item, flags = self.tree.HitTest(pt)

        if item:
            self.tree.item = item
            self.tree.item
            logger.debug("OnRightClick: %s, %s, %s" % (self.tree.GetItemText(item), type(item), item.__class__) + "\n")
            self.tree.SelectItem(item)
            if self.tree.GetItemText(self.tree.item) != 'Connections':
                logger.debug('parent %s', self.tree.GetItemText(self.tree.GetItemParent(self.tree.item)))

    #---------------------------------------------
    def OnTreeRightUp(self, event):
        event.Skip
       
        item = self.tree.item     
        
        if not item:
            event.Skip()
            return
        logger.debug('OnTreeRightUp')
        
        menu = wx.Menu()
        data = self.tree.GetItemData(item)
        rightClickDepth = data['depth']
        if rightClickDepth == 0:
            rootNewConnection = menu.Append(ID_ROOT_NEW_CONNECTION, "New connection ")
            
            refreshBmp = wx.MenuItem(menu, ID_ROOT_REFERESH, "&Refresh")
            refreshBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="database_refresh.png")))
            rootRefresh = menu.Append(refreshBmp)
            
            self.Bind(wx.EVT_MENU, self.onRootRefresh, rootRefresh)
            self.Bind(wx.EVT_MENU, self.onRootNewConnection, rootNewConnection)
        elif rightClickDepth == 1:
            if data['connection_name'] in self.connDict and \
                self.connDict[data['connection_name']]['isConnected']:
                item1 = menu.Append(ID_DISCONNECT_DB, "Disconnect")
                self.Bind(wx.EVT_MENU, self.onDisconnectDb, item1)
            else:
                item2 = menu.Append(ID_CONNECT_DB, "Connect")
                self.Bind(wx.EVT_MENU, self.onConnectDb, item2)
            
            sqlEditorBmp = wx.MenuItem(menu, ID_newWorksheet, "SQL Editor in new Tab")
            sqlEditorBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="script.png")))
            item3 = menu.Append(sqlEditorBmp)
            
            infoMenuItem = wx.MenuItem(menu, wx.ID_ANY, "Properties")
            infoBmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_MENU, (16, 16)) 
            infoMenuItem.SetBitmap(infoBmp)     
            item4 = menu.Append(infoMenuItem)    
            
            importBmp = wx.MenuItem(menu, ID_Import, "&Import CSV / Excel")
            importBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="import.png")))
            importMenu = menu.Append(importBmp)  
            
            refreshBmp = wx.MenuItem(menu, wx.ID_REFRESH, "&Refresh")
            refreshBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="database_refresh.png")))
            item5 = menu.Append(refreshBmp)
            
            item6 = menu.Append(wx.ID_ANY, "Properties")
            menu.AppendSeparator()
#             item7 = wx.MenuItem(menu, wx.ID_ANY, "&Smile!\tCtrl+S", "This one has an icon")
#             item7.SetBitmap(wx.Bitmap(os.path.abspath(os.path.join(path, "index.png"))))
#             menu.AppendItem(item7)
            
            deleteMenuItem = wx.MenuItem(menu, wx.ID_DELETE, "Delete reference \t Delete")
            delBmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_MENU, (16, 16))
            deleteMenuItem.SetBitmap(delBmp)
            delMenu = menu.Append(deleteMenuItem)
            
            deleteWithDatabaseMenuItem = wx.MenuItem(menu, ID_deleteWithDatabase, "Delete with database \t Shift + Delete")
            delBmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_MENU, (16, 16))
            deleteWithDatabaseMenuItem.SetBitmap(delBmp)
            deleteWithDatabaseMenu = menu.Append(deleteWithDatabaseMenuItem)
#             self.Bind(wx.EVT_MENU, self.OnItemBackground, item1)
            
            self.Bind(wx.EVT_MENU, self.onOpenSqlEditorTab, item3)
            self.Bind(wx.EVT_MENU, self.onProperties, item4)
            self.Bind(wx.EVT_MENU, self.onImport, importMenu)
            self.Bind(wx.EVT_MENU, self.onRefresh, item5)
            self.Bind(wx.EVT_MENU, self.onEditConnection, item6)
            self.Bind(wx.EVT_MENU, self.onDeleteConnection, delMenu)
            self.Bind(wx.EVT_MENU, self.onDeleteWithDatabaseTable, deleteWithDatabaseMenu)

        elif rightClickDepth == 2:
            if 'table' in self.tree.GetItemText(item):
                newTableBmp = wx.MenuItem(menu, wx.ID_ANY, "Create new table")
                newTableBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="table_add.png")))
                newTableItem = menu.Append(newTableBmp)                 
                
#                 newTableItem = menu.Append(wx.ID_ANY, "Create new table")
                erDiagramItem = menu.Append(wx.ID_ANY, "Create ER diagram")
                refreshTableItem = menu.Append(wx.ID_ANY, "Refresh  \tF5")
                
                self.Bind(wx.EVT_MENU, self.onNewTable, newTableItem)
                
                self.Bind(wx.EVT_MENU, self.onCreateErDiagramItem, erDiagramItem)
                
                self.Bind(wx.EVT_MENU, self.onRefreshTable, refreshTableItem)
                
            if 'view' in self.tree.GetItemText(item):
                newViewItem = menu.Append(wx.ID_ANY, "Create new view")
                item2 = menu.Append(wx.ID_ANY, "Refresh \tF5")
                self.Bind(wx.EVT_MENU, self.onNewView, newViewItem)
            if 'index' in self.tree.GetItemText(item) :
                newIndexItem = menu.Append(wx.ID_ANY, "Create new index")
                item2 = menu.Append(wx.ID_ANY, "Refresh \tF5")
                self.Bind(wx.EVT_MENU, self.onNewIndex, newIndexItem)
                
        elif 'Columns' in self.tree.GetItemText(item) :
            newColumnItem = menu.Append(wx.ID_ANY, "Add new column")
            self.Bind(wx.EVT_MENU, self.onNewColumn, newColumnItem)
            
        elif 'table' in self.tree.GetItemText(self.tree.GetItemParent(self.tree.item)) : 
            logger.debug(self.tree.GetItemText(item))

            editTableBmp = wx.MenuItem(menu, wx.ID_ANY, "Edit table")
            editTableBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="table_edit.png")))
            editTableItem = menu.Append(editTableBmp) 
            
#             editTableItem = menu.Append(wx.ID_ANY, "Edit table ")
            renameTableItem = menu.Append(wx.ID_ANY, "Rename Table ")
            copyCreateTableItem = menu.Append(wx.ID_ANY, "Copy create table statement")

            deleteTableBmp = wx.MenuItem(menu, wx.ID_ANY, "&Delete table ")
            deleteTableBmp.SetBitmap(wx.Bitmap(self.fileOperations.getImageBitmap(imageName="table_delete.png")))
            deleteTableItem = menu.Append(deleteTableBmp)

            self.Bind(wx.EVT_MENU, self.onDeleteTable, deleteTableItem)
            
            self.Bind(wx.EVT_MENU, self.onEditTable, editTableItem)
            self.Bind(wx.EVT_MENU, self.onRenameTable, renameTableItem)
            self.Bind(wx.EVT_MENU, self.onCopyCreateTableStatement, copyCreateTableItem)
            
        elif 'Column' in self.tree.GetItemText(self.tree.GetItemParent(self.tree.item)) : 
            logger.debug(self.tree.GetItemText(item))
            item1 = menu.Append(wx.ID_ANY, "Edit column")
            renameColumnItem = menu.Append(wx.ID_ANY, "Rename Column ")
#             item1 = menu.Append(wx.ID_ANY, "Create new column")
#             self.Bind(wx.EVT_MENU, self.OnItemBackground, item1)
            self.Bind(wx.EVT_MENU, self.onRenameColumn, renameColumnItem)
        
        self.PopupMenu(menu)
        menu.Destroy()

    def onDeleteTable(self, event):
        logger.debug('onDeleteTable')
        try:
#             data = self.tree.GetPyData(self.tree.GetSelection()).Data
            depth = self.tree.GetItemData(self.tree.GetSelection())['depth']
            ##################################################################################
            sqlExecuter = SQLExecuter(database='_opal.sqlite')
            textCtrl = self.GetTopLevelParent()._ctrl
            selectedItemText = textCtrl.GetValue()
            databaseAbsolutePath = sqlExecuter.getDbFilePath(selectedItemText)
            logger.debug("dbFilePath: %s", databaseAbsolutePath)
            
            ##################################################################################
    #         connectionName = data['connection_name']
#             databaseAbsolutePath = data['db_file_path']
            if os.path.isfile(databaseAbsolutePath) and depth == 3:     
                text = "DROP TABLE '{}'".format(self.tree.GetItemText(self.tree.GetSelection()))
                dbObjects = ManageSqliteDatabase(connectionName=selectedItemText , databaseAbsolutePath=databaseAbsolutePath).executeText(text)
                self.recreateTree(event) 
        except Exception as e:
            logger.error(e, exc_info=True)
    
    def onRefreshTable(self, event):
        logger.debug('onRefreshTable')

    def onRootRefresh(self, event):
        logger.debug('onRootRefresh')
        self.recreateTree(event)

    def onRootNewConnection(self, event):
        logger.debug('onRootNewConnection')
        CreateNewConncetionWixard(self).createWizard()
        
        # Refresh tree.
        
    def onCopyCreateTableStatement(self, event):
        logger.debug('onCopyCreateTableStatement')

    def onRenameColumn(self, event):
        logger.debug('onRenameColumn')
        initialColumnName = self.tree.GetItemText(self.tree.GetSelection())
        dlg = wx.TextEntryDialog(self, 'Rename column ' + initialColumnName, 'Rename column ' + initialColumnName, 'Python')
        dlg.SetValue(self.tree.GetItemText(self.tree.GetSelection()))

        if dlg.ShowModal() == wx.ID_OK:
            logger.info('You entered: %s\n', dlg.GetValue())
            if dlg.GetValue() != self.tree.GetItemText(self.tree.GetSelection()):
                logger.info('update table execute')
                data = self.tree.GetItemData(self.tree.GetSelection())
                connectionName = data['connection_name']
                databaseAbsolutePath = data['db_file_path']
                if os.path.isfile(databaseAbsolutePath):     
                    '''
                    First you rename the old table:
                    ALTER TABLE orig_table_name RENAME TO tmp_table_name;
                    Then create the new table, based on the old table but with the updated column name:
                    Then copy the contents across from the original table.
                    

                    '''
                    logger.debug("TODO logic for rename column goes here.")
#                     dbObjects = ManageSqliteDatabase(connectionName=connectionName , databaseAbsolutePath=databaseAbsolutePath).executeText(text) 
        dlg.Destroy()

#     def onDeleteConnection(self, event):
#         logger.debug('onDeleteConnection')
#         logger.debug("TODO delete connection name")
#         data = self.tree.GetItemData(self.tree.GetSelection())
#         connectionName = data['connection_name']
#         databaseAbsolutePath = data['db_file_path']
#         if os.path.isfile(databaseAbsolutePath):
#             sqlExecuter = SQLExecuter()
#             text="DELETE FROM conns WHERE {} "
#             sqlExecuter.executeText(text)
        
    def onRenameTable(self, event):
        logger.debug('onRenameTable')
        oldTableName = initialTableName = self.tree.GetItemText(self.tree.GetSelection())
        dlg = wx.TextEntryDialog(self, 'Rename table {} to'.format(initialTableName), 'Rename table {} '.format(initialTableName), 'Python')
        dlg.SetValue(self.tree.GetItemText(self.tree.GetSelection()))

        if dlg.ShowModal() == wx.ID_OK:
            logger.info('You entered: %s\n', dlg.GetValue())
            if dlg.GetValue() != self.tree.GetItemText(self.tree.GetSelection()):
                logger.info('update table execute')
                newTableName = dlg.GetValue()
                data = self.tree.GetItemData(self.tree.GetSelection())
                connectionName = data['connection_name']
                databaseAbsolutePath = data['db_file_path']
                if os.path.isfile(databaseAbsolutePath):     
                    '''
                    First you rename the old table:
                    '''
                    logger.debug("TODO logic to rename table should go here.")
#                     dropTableSql="DROP TABLE '{}'".format()
                    alterTableSql = "ALTER TABLE '{}' RENAME TO {}".format(oldTableName, newTableName)
                    db = ManageSqliteDatabase(connectionName=connectionName , databaseAbsolutePath=databaseAbsolutePath)
                    try:
                        db.executeText(alterTableSql)
                    except Exception as e:
                        self.consoleOutputLog(e)
            self.recreateTree(event)
        dlg.Destroy()
        
    def consoleOutputLog(self, exception=None):
        now = datetime.datetime.now()
        strftime = now.strftime("%Y-%m-%d %H:%M:%S")
        newline = "\n"
        if self.GetTopLevelParent()._mgr.GetPane("consoleOutput").window.text.Value.strip() == "":
            newline = ""
        self.GetTopLevelParent()._mgr.GetPane("consoleOutput").window.text.AppendText("{}{} {}".format(newline, strftime, exception))
    def onEditTable(self, event):
        logger.debug('onEditTable')

    def OnItemBackground(self, event):
        logger.debug('OnItemBackground')
        try:
            pt = event.GetPosition();
            item, flags = self.tree.HitTest(pt)
            self.tree.EditLabel(item)
        except Exception as e:
            logger.error(e, exc_info=True)

    def onConnectDb(self, event):
        logger.debug('onConnectDb')
#         item = self.tree.GetSelection() 
        try:
            if self.tree.GetItemText(self.tree.GetSelection()) not in self.connDict.keys():
                selectedItemId = self.tree.GetSelection()
                if self.getNodeOnOpenConnection(selectedItemId=selectedItemId):
        #         self.addNode(targetNode=, nodeLabel='got conncted',pydata=data, image=16)
                # Todo change icon to enable
                        selectedItemText = self.tree.GetItemText(self.tree.GetSelection())
                        self.setAutoCompleteText(selectedItemText)
                        self.openWorksheet(sheetName="Worksheet")
                self.connDict[self.tree.GetItemText(self.tree.GetSelection())] = {
                    'isConnected':True,
                    'data':self.tree.GetItemData(self.tree.GetSelection())
                    }
        except Exception as e:
            logger.error(e, exc_info=True)
    
    def setAutoCompleteText(self, selectedItemText):
        '''
        This is to set autocomplete text as we connect to database
        '''
        logger.debug(selectedItemText)
        if hasattr(self.GetTopLevelParent(), '_mgr'):
            tb1 = self.GetTopLevelParent()._mgr.GetPane("viewToolbar").window
            choice = self.GetTopLevelParent()._ctrl.GetChoices()
            textCtrl = self.GetTopLevelParent()._ctrl
            textCtrl.SetValue(selectedItemText)
    #         textCtrl.SetSelection(choice.index(selectedItemText))
            textCtrl.SetInsertionPointEnd()
            textCtrl.SetSelection(-1, -1)
            textCtrl._showDropDown(False)
    
    def onDisconnectDb(self, event):
        logger.debug('onDisconnectDb')
        del self.connDict[self.tree.GetItemText(self.tree.GetSelection())]
        selectedItem = self.tree.GetSelection()
        if selectedItem:
            self.tree.DeleteChildren(selectedItem)

            # Todo change icon to dissable
    def onOpenSqlEditorTab(self, event):
        logger.debug('onOpenSqlEditorTab')
        self.openWorksheet(sheetName="Worksheet")

    def openWorksheet(self, sheetName="Worksheet"):
        if hasattr(self.GetTopLevelParent(), '_mgr'):
            sqlExecutionTab = self.GetTopLevelParent()._mgr.GetPane("sqlExecution")
            if sqlExecutionTab.window:
                sqlExecutionTab.window.addTab(name=sheetName)
    
    def onProperties(self, event):
        logger.debug('onProperties')
        
    def onImport(self, event=None):
        logger.debug('onImport')
        selectedItem = self.tree.GetSelection()
        connectionName = self.tree.GetItemText(selectedItem)
        frame = ImportingCsvExcelFrame(None, 'Import CSV Excel', connectionName)
        frame.Show()
        
    def onRefresh(self, event=None):
        logger.debug('onRefresh')
        '''
        1. find current active connection.
        2. refresh only that connection.
        '''
        ##################################################################################
        sqlExecuter = SQLExecuter(database='_opal.sqlite')
        textCtrl = self.GetTopLevelParent()._ctrl
        selectedItemText = textCtrl.GetValue()
        dbFilePath = sqlExecuter.getDbFilePath(selectedItemText)
        logger.debug("dbFilePath: %s", dbFilePath)
        
        ##################################################################################
#         selectedItem = self.tree.GetSelection()
#         if selectedItem:
#             self.tree.DeleteChildren(selectedItem)        
#             self.getNodeOnOpenConnection(selectedItemId)
    def onEditConnection(self, event):
        logger.debug('onEditConnection')
        
    def onDeleteWithDatabaseTable(self, event):
        logger.debug('onDeleteWithDatabaseTable')
#         self.onDeleteConnection(event)
        ##################################################################################
        sqlExecuter = SQLExecuter(database='_opal.sqlite')
        selectedItemId = self.tree.GetSelection()
        selectedItemText = self.tree.GetItemText(self.tree.GetSelection())
        dbFilePath = sqlExecuter.getDbFilePath(selectedItemText)
        logger.debug("dbFilePath: %s", dbFilePath)
        
        ##################################################################################
        fileOperations = FileOperations()
        fileRemoved = fileOperations.removeFile(filename=dbFilePath)
        if selectedItemText and fileRemoved:
            self.sqlExecuter.removeConnctionRow(selectedItemText)
            self.recreateTree()

    def onDeleteConnection(self, event):
        logger.debug('onDeleteConnection')
        selectedItemId = self.tree.GetSelection()
        selectedItemText = self.tree.GetItemText(self.tree.GetSelection())
        logger.debug(selectedItemText)
        if selectedItemText:
            self.sqlExecuter.removeConnctionRow(selectedItemText)
            self.recreateTree()
            
    def onCreateErDiagramItem(self, event):
        logger.debug('onCreateErDiagramItem')
        ##################################################################################
        sqlExecuter = SQLExecuter(database='_opal.sqlite')
        textCtrl = self.GetTopLevelParent()._ctrl
        selectedItemText = textCtrl.GetValue()
        dbFilePath = sqlExecuter.getDbFilePath(selectedItemText)
        logger.debug("dbFilePath: %s", dbFilePath)
        
        ################################################################################## 
        depth = self.tree.GetItemData(self.tree.GetSelection())['depth']   
        if os.path.isfile(dbFilePath):     
            dbObjects = ManageSqliteDatabase(connectionName=selectedItemText , databaseAbsolutePath=dbFilePath).getObject()   
             
        createErDiagramFrame = CreateErDiagramFrame(None)
        createErDiagramFrame.setDbObjects(dbObjects=dbObjects)
        createErDiagramFrame.Show()        

    def onNewTable(self, event):
        logger.debug('onNewTable')
        item = self.tree.item  
        connectionName = self.tree.GetItemText(self.tree.GetItemParent(item))
        
        newTableName = SQLUtils().definingTableName(connectionName)
        
        tableFrame = CreatingTableFrame(None, 'Table creation', connectionName, newTableName)
#         frame = CreateTableFrame(None, 'table creation')
    
#         tableDict = dict()
#         tableFrame.setData(tableDict)
        tableFrame.Show()
#         app.MainLoop()
        
    def onNewView(self, event):
        logger.debug('onNewView')

#         tableFrame = CreateTableFrame(None, 'Table creation')
    def onNewColumn(self, event):
        logger.debug('onNewColumn')
        logger.debug("TODO add a new column")

    def onNewIndex(self, event):
        logger.debug('onNewIndex')
        logger.debug("TODO add a new Index")
#         tableFrame = CreateTableFrame(None, 'Table creation')
        
    def getNodeOnOpenConnection(self, selectedItemId=None, data=None):
        '''
        This method will return database node on open connection
        '''
        isSuccessfullyConnected = False
        logger.debug('getNodeOnOpenConnection')
        if selectedItemId:
            data = self.tree.GetItemData(selectedItemId)
        connectionName = data['connection_name']
        databaseAbsolutePath = data['db_file_path']
        if os.path.isfile(databaseAbsolutePath):     
            dbObjects = ManageSqliteDatabase(connectionName=connectionName , databaseAbsolutePath=databaseAbsolutePath).getObject() 
            isSuccessfullyConnected = True
            for dbObject in dbObjects[1]:
                for k0, v0 in dbObject.items():
                    logger.debug("k0 : %s, v0: %s", k0, v0)
                    data = dict()
                    data['depth'] = 2
                    data['connection_name'] = connectionName
                    data['db_file_path'] = databaseAbsolutePath
                    image = 2
                    nodeLabel = k0 + ' (' + str(len(v0)) + ')'
                    
                    child0 = self.addNode(targetNode=selectedItemId, nodeLabel=nodeLabel, pydata=data, image=image) 
                    if 'table' == k0 :
                        # setting image for 'table'
                        image = 4
                    elif 'index' == k0 :
                        # setting image for 'index'
                        image = 5
                    elif 'view' == k0 :
                        # setting image for 'view'
                        image = 6
    #                 child = self.tree.AppendItem(selectedItemId, k0 + ' (' + str(len(items)) + ')', image=count)
                    for v00 in v0:
                        for k1, v1 in v00.items():
                            # Listing tables
                            data = dict()
                            data['depth'] = 3
                            data['connection_name'] = connectionName
                            data['db_file_path'] = databaseAbsolutePath
                            nodeLabel = k1 
                            if k0 == 'table':
                                image = 4
                            child1 = self.addNode(targetNode=child0, nodeLabel=nodeLabel, pydata=data, image=image) 
                            
#                             logger.debug("k1 : %s, v1: %s", k1, v1)
                            if k0 == 'table':
                                data = dict()
                                data['depth'] = 4
                                data['connection_name'] = connectionName
                                data['db_file_path'] = databaseAbsolutePath
                                # setting  image for 'Columns', 'Unique Keys', 'Foreign Keys', 'References'
                                image = 11
                                
                                child1_1 = self.addNode(targetNode=child1, nodeLabel='Columns' + ' (' + str(len(v1)) + ')', pydata=data, image=image) 
                                child1_2 = self.addNode(targetNode=child1, nodeLabel='Unique Keys', pydata=data, image=image) 
                                child1_3 = self.addNode(targetNode=child1, nodeLabel='Foreign Keys', pydata=data, image=image) 
                                child1_4 = self.addNode(targetNode=child1, nodeLabel='References', pydata=data, image=image) 
                            for v2 in v1:
                                if k0 == 'table':
                                    data = dict()
                                    data['depth'] = 5
                                    data['connection_name'] = connectionName
                                    data['db_file_path'] = databaseAbsolutePath
    #                                  (cid integer, name text, type text, nn bit, dflt_value, pk bit)
                                    nodeLabel = v2[1]
                                    image = 18
                                    if v2[5] == 1:
                                        # setting primary key image
                                        image = 9
                                    elif v2[5] == 0 and v2[2] in ['INTEGER', 'INT']:
                                        # setting INTEGER image
                                        image = 7
                                    elif v2[5] == 0 :
                                        for datatype in ['VARCHAR', 'CHAR', 'REAL', 'TEXT']:
                                            if v2[2].lower().startswith(datatype.lower()):
                                                # setting VARCHAR image
                                                image = 18
                                                break
                                    child2 = self.addNode(targetNode=child1_1, nodeLabel=nodeLabel, pydata=data, image=image) 
        else:
            updateStatus = "Unable to connect '" + databaseAbsolutePath + ".' No such file. "
            self.consoleOutputLog(updateStatus)
            font = self.GetTopLevelParent().statusbar.GetFont() 
            font.SetWeight(wx.BOLD) 
            self.GetTopLevelParent().statusbar.SetFont(font) 
            self.GetTopLevelParent().statusbar.SetForegroundColour(wx.RED) 
            self.GetTopLevelParent().statusbar.SetStatusText(updateStatus, 1)
            logger.error(updateStatus)
            
        return isSuccessfullyConnected

        
class DatabaseNavigationTree(ExpansionState, TreeCtrl):
    '''
    Left navigation tree in database page
    '''

    def __init__(self, parent):
        TreeCtrl.__init__(self, parent, style=wx.TR_DEFAULT_STYLE | 
                               wx.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.BuildTreeImageList()
        
#         if USE_CUSTOMTREECTRL:
#             self.SetSpacing(10)
#             self.SetWindowStyle(self.GetWindowStyle() & ~wx.TR_LINES_AT_ROOT)
        self.eventdict = {
#                           'EVT_TREE_BEGIN_DRAG': self.OnBeginDrag, 'EVT_TREE_BEGIN_LABEL_EDIT': self.OnBeginEdit,
#                           'EVT_TREE_BEGIN_RDRAG': self.OnBeginRDrag, 'EVT_TREE_DELETE_ITEM': self.OnDeleteItem,
#                           'EVT_TREE_END_DRAG': self.OnEndDrag, 'EVT_TREE_END_LABEL_EDIT': self.OnEndEdit,
#                           'EVT_TREE_ITEM_ACTIVATED': self.OnActivate, 'EVT_TREE_ITEM_CHECKED': self.OnItemCheck,
#                           'EVT_TREE_ITEM_CHECKING': self.OnItemChecking, 'EVT_TREE_ITEM_COLLAPSED': self.OnItemCollapsed,
#                           'EVT_TREE_ITEM_COLLAPSING': self.OnItemCollapsing, 'EVT_TREE_ITEM_EXPANDED': self.OnItemExpanded,
#                           'EVT_TREE_ITEM_EXPANDING': self.OnItemExpanding, 'EVT_TREE_ITEM_GETTOOLTIP': self.OnToolTip,
#                           'EVT_TREE_ITEM_MENU': self.OnItemMenu, 'EVT_TREE_ITEM_RIGHT_CLICK': self.OnRightDown,
                            'EVT_TREE_KEY_DOWN': self.OnKey,
#                           'EVT_TREE_SEL_CHANGED': self.OnSelChanged,
#                           'EVT_TREE_SEL_CHANGING': self.OnSelChanging, "EVT_TREE_ITEM_HYPERLINK": self.OnHyperLink
                          }
        self.SetInitialSize((100, 80))
            
    def AppendItem(self, parent, text, image=-1, wnd=None):

        item = TreeCtrl.AppendItem(self, parent, text, image=image)
        return item
    #---------------------------------------------

    def OnKey(self, event):
        logger.debug('onkey')
        keycode = event.GetKeyCode()
        keyname = keyMap.get(keycode, None)
                
        if keycode == wx.WXK_BACK:
            logger.debug("OnKeyDown: HAHAHAHA! I Vetoed Your Backspace! HAHAHAHA\n")
            return

        if keyname is None:
            if "unicode" in wx.PlatformInfo:
                keycode = event.GetUnicodeKey()
                if keycode <= 127:
                    keycode = event.GetKeyCode()
                keyname = "\"" + event.GetUnicodeKey() + "\""
                if keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode - 1)
                
            elif keycode < 256:
                if keycode == 0:
                    keyname = "NUL"
                elif keycode < 27:
                    keyname = "Ctrl-%s" % chr(ord('A') + keycode - 1)
                else:
                    keyname = "\"%s\"" % chr(keycode)
            else:
                keyname = "unknown (%s)" % keycode
                
        logger.debug("OnKeyDown: You Pressed : %s", keyname)

        event.Skip()            

    def BuildTreeImageList(self):
        logger.debug('BuildTreeImageList')
        self.fileOperations = FileOperations()
        imgList = wx.ImageList(16, 16)

        # add the image for modified demos.

        imgList.Add(self.fileOperations.getImageBitmap(imageName="database.png"))  # 0
        imgList.Add(self.fileOperations.getImageBitmap(imageName="database_category.png"))  # 1
        imgList.Add(self.fileOperations.getImageBitmap(imageName="folder_view.png"))  # 2
        imgList.Add(self.fileOperations.getImageBitmap(imageName="folder.png"))  # 3
        imgList.Add(self.fileOperations.getImageBitmap(imageName="table.png"))  # 4
        imgList.Add(self.fileOperations.getImageBitmap(imageName="view.png"))  # 5
        imgList.Add(self.fileOperations.getImageBitmap(imageName="index.png"))  # 6
        imgList.Add(self.fileOperations.getImageBitmap(imageName="column.png"))  # 7 using to show integer column 
        imgList.Add(self.fileOperations.getImageBitmap(imageName="string.png"))  # 8
        imgList.Add(self.fileOperations.getImageBitmap(imageName="key.png"))  # 9
        imgList.Add(self.fileOperations.getImageBitmap(imageName="foreign_key_column.png"))  # 10
        imgList.Add(self.fileOperations.getImageBitmap(imageName="columns.png"))  # 11
        imgList.Add(self.fileOperations.getImageBitmap(imageName="unique_constraint.png"))  # 12
        imgList.Add(self.fileOperations.getImageBitmap(imageName="reference.png"))  # 13
        imgList.Add(self.fileOperations.getImageBitmap(imageName="datetime.png"))  # 14
        imgList.Add(self.fileOperations.getImageBitmap(imageName="columns.png"))  # 15
        imgList.Add(self.fileOperations.getImageBitmap(imageName="sqlite.png"))  # 16
        imgList.Add(self.fileOperations.getImageBitmap(imageName="h2.png"))  # 17 use to show h2 database icon
        imgList.Add(self.fileOperations.getImageBitmap(imageName="textfield.png"))  # 18 use to show [varchar, char, text data] type icon 
        
#         imgList.Add(wx.Bitmap(path2))
#         for png in _demoPngs:
#             imgList.Add(catalog[png].GetBitmap())

        self.AssignImageList(imgList)

    def GetItemIdentity(self, item):
        return self.GetItemData(item)

    def Freeze(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(DatabaseNavigationTree, self).Freeze()
                         
    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(DatabaseNavigationTree, self).Thaw()
#---------------------------------------------------------------------------


class MainPanel(wx.Panel):
    """
    Just a simple derived panel where we override Freeze and Thaw so they are
    only used on wxMSW.    
    """

    def Freeze(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(MainPanel, self).Freeze()
                         
    def Thaw(self):
        if 'wxMSW' in wx.PlatformInfo:
            return super(MainPanel, self).Thaw()


class MyFileDropTarget(wx.FileDropTarget):

    def __init__(self, dirwin):
        wx.FileDropTarget.__init__(self)
        self.dirwin = dirwin

    def OnDropFiles(self, x, y, fileNams):
        logger.debug("dropFiles {}".format(fileNams))
        
        try:
            for fileAbsoluteName in fileNams:
                if os.path.isdir(fileAbsoluteName):
                    continue
                logger.debug(fileAbsoluteName)
                if self.isSQLite3(fileAbsoluteName):
                    self.getConnectionName(filePath=fileAbsoluteName)
                    sqlExecuter = SQLExecuter()
                    obj = sqlExecuter.getObject()
                    if len(obj[1]) == 0:
                        sqlExecuter.createOpalTables()
                    sqlExecuter.addNewConnectionRow(fileAbsoluteName, self.getConnectionName(filePath=fileAbsoluteName))
                    self.dirwin.recreateTree()           
        except Exception as ex:
            logger.error(ex)
              
        return True

    def getConnectionName(self, filePath=None):
        head, tail = ntpath.split(filePath)
        connectionName = "_".join(tail.split(sep=".")[:-1])
        return connectionName
    
    def isSQLite3(self, fileName):
        ''' this is to check a valid SQLite file dropped.
        '''
        from os.path import isfile, getsize
    
        if not isfile(fileName):
            return False
        if getsize(fileName) < 100:  # SQLite database file header is 100 bytes
            return False
    
        with open(fileName, 'rb') as fd:
            header = fd.read(100)
    
        return header[:16] == b'SQLite format 3\x00'
#                 self.dirwin.addpath(filename)
#                 if Globals.pref.open_project_setting_dlg:
#                     wx.CallAfter(self.dirwin.OnSetProject)
#             else:
#                 Globals.mainframe.editctrl.new(filename)


#---------------------------------------------------------------------------
if __name__ == '__main__':
#     treeImageLevel = dict()
#     treeImageLevel[(0, 0)] = (0, 'database.png')
#     treeImageLevel[(1, 0)] = (0, 'database_category.png')
#     treeImageLevel[(1, 1)] = (0, 'folder_view.png')
#     treeImageLevel[(1, 2)] = (0, 'folder.png')
#     
#     print(treeImageLevel[(0, 0)])
    app = wx.App(False)
    frame = wx.Frame(None)
    try: 
        panel = CreatingTreePanel(frame, preferenceName='asfd')
    except Exception as ex:
        logger.error(ex)
    frame.Show()
    app.MainLoop()
