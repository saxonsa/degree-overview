(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-51746d99"],{4645:function(t,e,n){"use strict";n("ba0e")},ba0e:function(t,e,n){},fc13:function(t,e,n){"use strict";n.r(e);var s=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"reset_password"}},[n("v-container",{staticClass:"fill-height justify-center"},[n("v-row",{staticClass:"mx-auto"},[n("v-col",{attrs:{cols:"12","offset-md":"2",md:"8"}},[n("v-slide-y-transition",[n("v-card",{attrs:{md:"3",light:""}},[n("pages-heading",{staticClass:"text-center display-3"},[t._v(" Get your password back ")]),n("hr"),n("v-row",[n("v-col",{attrs:{cols:"12",md:"6"}},[n("v-row",{attrs:{"no-gutters":""}},t._l(t.sections,(function(e,s){return n("v-col",{key:s,attrs:{cols:"12"}},[n("v-list-item",{attrs:{"three-line":""}},[n("v-list-item-icon",{staticClass:"mr-4 mt-5 mt-md-4"},[n("v-icon",{attrs:{large:t.$vuetify.breakpoint.mdAndUp,color:e.iconColor},domProps:{textContent:t._s(e.icon)}})],1),n("v-list-item-content",[n("v-list-item-title",{staticClass:"font-weight-light mb-4 mt-3",domProps:{textContent:t._s(e.title)}}),n("v-list-item-subtitle",{domProps:{textContent:t._s(e.text)}})],1)],1)],1)})),1)],1),n("v-col",{attrs:{cols:"12",md:"6"}},[n("div",{staticClass:"text-center"},[n("v-text-field",{staticStyle:{"margin-top":"40px"},attrs:{color:"secondary",label:"Username...","prepend-icon":"mdi-face",rules:[function(t){return!!t||"Please input username"}]},model:{value:t.username,callback:function(e){t.username=e},expression:"username"}}),n("v-text-field",{attrs:{color:"secondary",label:"Email to send instruction...","prepend-icon":"mdi-email",rules:[function(t){return!!t||"Please input your email"}]},model:{value:t.email,callback:function(e){t.email=e},expression:"email"}}),n("pages-btn",{staticStyle:{"margin-top":"25px"},attrs:{color:"#81C784"},on:{click:t.findPassword}},[t._v(" Find Password ")]),n("div",{staticClass:"text-center grey--text body-1 font-weight-light",staticStyle:{"margin-top":"5%"}},[t._v(" Remember your password? Go to "),n("a",{attrs:{href:"/login"}},[t._v("Login")])])],1)])],1)],1)],1)],1)],1)],1)],1)},i=[],o=(n("d3b7"),n("3ca3"),n("ddb0"),n("c24f")),a={name:"ResetPassword",components:{PagesBtn:function(){return n.e("chunk-2d0ea0b7").then(n.bind(null,"8fb5"))},PagesHeading:function(){return n.e("chunk-2d0f014c").then(n.bind(null,"9b9f"))}},data:function(){return{sections:[{icon:"mdi-chart-timeline-variant",iconColor:"primary",title:"User manual",text:"1. Please confirm the username is yourself, or there maybe some troubles happen."},{icon:"mdi-code-tags",iconColor:"secondary",text:"2. After you click the 'Find password' button, you will receive an email on your input email."},{icon:"mdi-account-multiple",iconColor:"cyan",text:"3. Please follow the instruction to get your password back."}],username:"",email:""}},methods:{findPassword:function(){var t=this;console.log("username",this.username),console.log("email",this.email),this.username&&this.email&&Object(o["c"])({username:this.username,email:this.email}).then((function(e){console.log(e),t.$store.dispatch("openSnackBar",{msg:"Reset function will be provided by ITSC, not our DegreeOverview system !!!",color:"#FFD54F",closeBtnColor:"#FFCC80"})}))}}},r=a,l=(n("4645"),n("2877")),c=n("6544"),m=n.n(c),d=n("b0af"),u=n("62ad"),f=n("a523"),p=n("132d"),v=n("da13"),b=n("5d23"),h=n("34c3"),g=n("0fd9"),y=n("0789"),w=n("8654"),C=Object(l["a"])(r,s,i,!1,null,"b7a4ec1e",null);e["default"]=C.exports;m()(C,{VCard:d["a"],VCol:u["a"],VContainer:f["a"],VIcon:p["a"],VListItem:v["a"],VListItemContent:b["a"],VListItemIcon:h["a"],VListItemSubtitle:b["b"],VListItemTitle:b["c"],VRow:g["a"],VSlideYTransition:y["e"],VTextField:w["a"]})}}]);
//# sourceMappingURL=chunk-51746d99.2666db1e.js.map