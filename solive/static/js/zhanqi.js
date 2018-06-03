$(document).ready(function(){
  var ui = {};
  ui.$win = $(window);
  ui.$room_list_tabs = $('.js-room-list-tabs');
  ui.$loading = $('.list-loading');
  ui.room_list_html = $('#dataForamt').html();

  var oPage = {
    listHash: {}
  , init: function(){
      ui.$room_list_tabs.find('.js-room-list-tabc .js-room-list-ul').videoHover({ hover: '.js-jump-link' });

      var $activeList = this.fActiveList();
      if( $activeList.length && 'iframe' != $activeList.data('type') ){
        $activeList.find('.js-room-list-ul').listAutofix();
        this.fWhenListActive($activeList);
      }

      this.view();
      this.bindEvent();
    }
  , view: function(){}
  , bindEvent: function(){
      var self = this;

      // 设定滚动事件
      var srollEvent = 'scroll.load.';
      ui.$win.on( srollEvent, function(){
        var $activeList = self.fActiveList();
        if( $activeList.data('ajaxing') ){
          return false;
        }
        var scrollTop = ui.$win.scrollTop()
          , winHeight = yp.global.height
          , top = ui.$win[0].document.body.clientHeight;
        if( winHeight + scrollTop + 70 >= top) {
          self.fLoadList($activeList);
        }
      });

      ui.$room_list_tabs.on('tabsactive', function(e){
        var $activeList = self.fActiveList();
        $activeList.find('.js-room-list-ul').listAutofix();
        self.fWhenListActive($activeList);
      });

      yp.sub('ui/resize', function(){
        var $activeList = self.fActiveList();
        $activeList.find('.js-room-list-ul').listAutofix();
      });

      yp.sub('page/leftpanel/collapse', function(){
        var $activeList = self.fActiveList();
        $activeList.find('.js-room-list-ul').listAutofix();
      });

      $('.js-cj-list').on('click', '.js-eatchicken-a', function() {
        var key = $(this).data('cjtongji');
        if( !!key ) {
          mfTongji('eat_chicken', 'room_'+key+'_click');
        }
      })
    }
    // 获取当前显示的列表
  , fActiveList: function(){
      if(gameId == 106) {
        return ui.$room_list_tabs.find('.js-cj-list.active');
      }
      return ui.$room_list_tabs.find('.js-room-list-tabc.active');
    }
    // 列表显示了
    // 判断是否要加载第一页
  , fWhenListActive: function($activeList){
      var self = this;

      if( 'iframe' == $activeList.data('type') ){
        return false;
      }

      if( !self.listHash[$activeList.data('type')] ){
        self.listHash[$activeList.data('type')] = { curPage: 0, size: $activeList.data('size'), url: $activeList.data('url'), end: false, cnt: $activeList.data('cnt') || 0 };
        if( 0 < $activeList.data('curPage') ){
          self.listHash[$activeList.data('type')]['curPage'] = $activeList.data('curPage');
          self.fGetFirstPageRoomCjInfo($activeList);
        } else {
          self.fLoadList($activeList, true);
        }
      }
    }
    // 获取直播间列表
  , fLoadList: function($activeList, bFirst){
      var self = this
        , $list = $activeList.find('.js-room-list-ul')
        , type = $activeList.data('type');
      var oListInfo = self.listHash[type];
      if( !oListInfo || $activeList.data('ajaxing') || oListInfo.end ){
        return false;
      }

      if( !bFirst && !oListInfo.end ){
        // 计算是否最后一页
        oListInfo.end = ( Math.ceil( oListInfo.cnt / oListInfo.size ) <= oListInfo.curPage );
      }
      if( oListInfo.end ){
        if( self.oDataCatch[ type ] && self.oDataCatch[ type ]['rooms'].length ){
          self.fAppendHtml($list, type, oListInfo.size);
        }
        return false;
      }

      ui.$loading.show();
      $activeList.data('ajaxing', true);
      var url = yp.format(oListInfo.url, { page: oListInfo.curPage + 1, size: oListInfo.size });
      yp.ajax(url, {
        type: 'get'
      , dataType: 'json'
      }).always(function(){
        $activeList.data('ajaxing', false);
        ui.$loading.hide();
      }).done(function(data){
        if( 0 == data.code ){
          oListInfo.curPage++;
          oListInfo.cnt = data.data.cnt;

          if( 0 < oListInfo.cnt ){
            !self.oDataCatch[ type ] && ( self.oDataCatch[ type ] = { got: [], rooms: [] } );
            yp.each(data.data.rooms, function(one){
              if( !$list.find('li[data-room-id="' + one.id + '"]').length && -1 == $.inArray(one.id, self.oDataCatch[ type ]['got']) ){
                self.oDataCatch[ type ]['got'].push(one.id);
                self.oDataCatch[ type ]['rooms'].push(one);
              }
            });

            // 判断是否是最后一页
            if( Math.ceil( oListInfo.cnt / oListInfo.size ) <= oListInfo.curPage ){
              self.fAppendHtml($list, type, oListInfo.size);
            } else {
              if( oListInfo.size <= self.oDataCatch[ type ]['rooms'].length ){
                self.fAppendHtml($list, type, oListInfo.size);
              } else {
                self.fLoadList($activeList, bFirst);
              }
            }
          } else {
            $list.after('<p class="no-videoList-title">当前没有主播直播</p>');
          }
        }
      });
    }
  , oDataCatch: {}
  , fAppendHtml: function($list, type, size){
      var self = this
        , sHtml = ''
        , i = 0
        , cjRoomIdList = []
        , cjPeople = 0
        , cjClassname = ''
        , cjHidden = ''
        , cjType = ''
        , cjUnit = '人'
        , cjTongji = ''
        , typeArr = ['alive', 'kill', 'survived', 'solo']
        , servers = ['', '亚服', '北美', '南美', '欧服', '东南亚', '大洋洲'];

      while( self.oDataCatch[type]['rooms'].length && 30 > i ){
        if (oPageConfig.aCjGameIdList.indexOf(self.oDataCatch[type]['rooms'][0].gameId + '') >= 0) {
          cjRoomIdList.push(self.oDataCatch[type]['rooms'][0].id);
        }

        self.oDataCatch[type]['rooms'][0].gender = (2 == self.oDataCatch[type]['rooms'][0].gender) ? 'sex-man' : 'sex-woman';
        if( 1000000 < self.oDataCatch[type]['rooms'][0].online ){
          self.oDataCatch[type]['rooms'][0].online = ( +self.oDataCatch[type]['rooms'][0].online / 10000 ).toFixed(0) + '万';
        } else if( 10000 < self.oDataCatch[type]['rooms'][0].online ){
          self.oDataCatch[type]['rooms'][0].online = ( +self.oDataCatch[type]['rooms'][0].online / 10000 ).toFixed(1) + '万';
        }
        // 2018.03.19新增标签
        if(self.oDataCatch[type]['rooms'][0].tags.common.pcIcon) {
          self.oDataCatch[type]['rooms'][0].commonIcon = self.oDataCatch[type]['rooms'][0].tags.common.pcIcon;
          self.oDataCatch[type]['rooms'][0].commonType = '';
        }else {
          self.oDataCatch[type]['rooms'][0].commonIcon = '';
          self.oDataCatch[type]['rooms'][0].commonType = 'hidden';
        }
        if(self.oDataCatch[type]['rooms'][0].tags.system.pcIcon) {
          self.oDataCatch[type]['rooms'][0].systemIcon = self.oDataCatch[type]['rooms'][0].tags.system.pcIcon;
          self.oDataCatch[type]['rooms'][0].systemType = '';
        }else {
          self.oDataCatch[type]['rooms'][0].systemIcon = '';
          self.oDataCatch[type]['rooms'][0].systemType = 'hidden';
        }
        if(gameId == 106) {
          switch(type) {
            case 'kill':
              cjPeople = self.oDataCatch[type]['rooms'][0].killNumber;
              cjClassname = 'kill';
              cjType = 'kill';
              cjTongji = 'kill';
              break;
            case 'survived':
              cjPeople = self.oDataCatch[type]['rooms'][0].timeSurvived;
              cjClassname = 'eat-chicken';
              cjType = '吃鸡';
              cjUnit = '次';
              cjTongji = 'eat';
              break;
            case 'solo':
              cjPeople = self.oDataCatch[type]['rooms'][0].solo;
              cjType = servers[self.oDataCatch[type]['rooms'][0].server];
              cjClassname = cjType.length == 3 ? 'big-rank' : 'rank';
              cjUnit = '';
              cjTongji = 'grid';
              if(self.oDataCatch[type]['rooms'][0].server == 0) {
                cjHidden = 'hidden';
              }
              break;
            default:
              if(type == 'alive') {
                cjTongji = 'servival';
              }
              if(self.oDataCatch[type]['rooms'][0].alive) {
                cjPeople = self.oDataCatch[type]['rooms'][0].alive;
                cjClassname = cjPeople <= 20 ? 'little-survive' : '';
                cjType = '存活';
              }else {
                cjHidden = 'hidden';
              }
              break;
          }
          self.oDataCatch[type]['rooms'][0].cjhidden = cjPeople <= 0 ? 'hidden' : cjHidden;
          self.oDataCatch[type]['rooms'][0].cjpeople = cjPeople > 9999 ? '9999+' : cjPeople;
          self.oDataCatch[type]['rooms'][0].cjclassname = cjClassname;
          self.oDataCatch[type]['rooms'][0].cjtype = cjType;
          self.oDataCatch[type]['rooms'][0].cjunit = cjUnit;
          self.oDataCatch[type]['rooms'][0].cjtongji = cjTongji;
          if(type != 'all') {
            // 4个榜单不显示标签
            self.oDataCatch[type]['rooms'][0].commonType = 'hidden';
            self.oDataCatch[type]['rooms'][0].systemType = 'hidden';
          }
        }else{
          self.oDataCatch[type]['rooms'][0].cjhidden = 'hidden';
        }
        // end
        sHtml += yp.format( ui.room_list_html, self.oDataCatch[type]['rooms'][0] );

        self.oDataCatch[type]['rooms'].shift();
        i++;
      }

      var sizeIndex = $list.find('li').length;
      $list.append(sHtml);
      $list.listAutofix( sizeIndex );

      if($.inArray(type, typeArr) != -1) {
        return false;
      }
      self.fGetEatChickenInfo(cjRoomIdList, $list);
    }
    // fGetFirstPageRoomCjInfo: 获取第一页吃鸡信息
  , fGetFirstPageRoomCjInfo: function ($list) {
      var self = this;
      var roomIdArr = [];

      if(!oPageConfig.aFirstPageCjRooms || !oPageConfig.aFirstPageCjRooms.length){
        return false;
      }

      yp.each($list.find('li'), function (room) {
        var $room = $(room)
          , roomId = $room.attr('data-room-id') + '';

        if(oPageConfig.aFirstPageCjRooms.indexOf(roomId) >= 0){
          roomIdArr.push(roomId);
        }
      });

      self.fGetEatChickenInfo(roomIdArr, $list);
    }

    // fGetEatChickenInfo: 异步更新吃鸡人数标签
    // @params:
    //   roomIdList: 房间id列表
    //   $list: 需要更新的list
  , fGetEatChickenInfo: function (roomIdList, $list) {
      if(!roomIdList.length){
        return false;
      }
      yp.ajax('/api/touch/live/cj', {
        data: {roomIds: roomIdList.join(',')}
      }).done(function (res) {
        if (+res.code === 0) {
          yp.each(res.data, function (cjInfo) {
            var $cjArea = $list.find('li[data-room-id="' + cjInfo.roomId + '"]');

            $cjArea.find('.js-txt-eat-chicken-num').html(cjInfo.alive);
            $cjArea.find('.js-div-eat-chicken').toggleClass('little-survive', cjInfo.alive <= 20).show();
          });
        }
      });
    }
  };
  oPage.init();
});

yp.use('tabs');