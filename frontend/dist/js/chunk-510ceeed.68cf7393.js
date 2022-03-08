(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-510ceeed"],{"075a":function(t,e,i){"use strict";i("7bdd")},5311:function(t,e,i){"use strict";var n=i("5607"),s=i("2b0e");e["a"]=s["default"].extend({name:"rippleable",directives:{ripple:n["a"]},props:{ripple:{type:[Boolean,Object],default:!0}},methods:{genRipple:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return this.ripple?(t.staticClass="v-input--selection-controls__ripple",t.directives=t.directives||[],t.directives.push({name:"ripple",value:{center:!0}}),this.$createElement("div",t)):null}}})},"6ca7":function(t,e,i){},"7bdd":function(t,e,i){},8547:function(t,e,i){"use strict";var n=i("2b0e"),s=i("80d2");e["a"]=n["default"].extend({name:"comparable",props:{valueComparator:{type:Function,default:s["h"]}}})},ea85:function(t,e,i){"use strict";i.r(e);var n=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{attrs:{id:"register"}},[i("v-container",{staticClass:"fill-height justify-center"},[i("v-row",{staticClass:"mx-auto"},[i("v-col",{attrs:{cols:"12","offset-md":"2",md:"8"}},[i("v-slide-y-transition",[i("v-card",{attrs:{md:"3",light:""}},[i("pages-heading",{staticClass:"text-center display-3"},[t._v(" Join Daffodil now ")]),i("v-row",[i("v-col",{attrs:{cols:"12",md:"6"}},[i("v-row",{attrs:{"no-gutters":""}},t._l(t.sections,(function(e,n){return i("v-col",{key:n,attrs:{cols:"12"}},[i("v-list-item",{attrs:{"three-line":""}},[i("v-list-item-icon",{staticClass:"mr-4 mt-5 mt-md-4"},[i("v-icon",{attrs:{large:t.$vuetify.breakpoint.mdAndUp,color:e.iconColor},domProps:{textContent:t._s(e.icon)}})],1),i("v-list-item-content",[i("v-list-item-title",{staticClass:"font-weight-light mb-4 mt-3",domProps:{textContent:t._s(e.title)}}),i("v-list-item-subtitle",{domProps:{textContent:t._s(e.text)}})],1)],1)],1)})),1)],1),i("v-col",{attrs:{cols:"12",md:"6"}},[i("div",{staticClass:"text-center"},[i("v-text-field",{attrs:{color:"secondary",label:"Nickname...","prepend-icon":"mdi-face",rules:[function(t){return!!t||"Please input nick name"}]},model:{value:t.nickname,callback:function(e){t.nickname=e},expression:"nickname"}}),i("v-text-field",{attrs:{color:"secondary",label:"Username...","prepend-icon":"mdi-account",rules:[function(t){return!!t||"Please input your user name"}]},model:{value:t.username,callback:function(e){t.username=e},expression:"username"}}),i("v-text-field",{attrs:{color:"secondary",label:"Password...","prepend-icon":"mdi-lock-outline",type:"password",rules:[function(t){return!!t||"Please input your password"}]},model:{value:t.password,callback:function(e){t.password=e},expression:"password"}}),i("v-text-field",{staticClass:"mb-8",attrs:{color:"secondary",label:"Confirm Password...","prepend-icon":"mdi-lock",type:"password",rules:[function(t){return!!t||"Please input your password again"}]},model:{value:t.confirmPassword,callback:function(e){t.confirmPassword=e},expression:"confirmPassword"}}),i("v-checkbox",{attrs:{"input-value":t.checkAgreement,color:"secondary"},scopedSlots:t._u([{key:"label",fn:function(){return[i("span",{staticClass:"text-no-wrap",staticStyle:{"margin-top":"5px"},domProps:{innerHTML:t._s(t.agreeText)}}),i("a",{staticClass:"secondary--text ml-6 ml-sm-0 text-no-wrap",staticStyle:{"margin-top":"5px"},attrs:{href:"#"}},[t._v(" terms and conditions ")]),t._v(". ")]},proxy:!0}])}),i("pages-btn",{attrs:{color:"#81C784"},on:{click:t.register}},[t._v(" Get Started ")]),i("div",{staticClass:"text-center grey--text body-1 font-weight-light",staticStyle:{"margin-top":"5%"}},[t._v(" Already have an account? Go to "),i("a",{attrs:{href:"/login"}},[t._v("Login")])])],1)])],1)],1)],1)],1)],1)],1)],1)},s=[],a=(i("d3b7"),i("3ca3"),i("ddb0"),i("c24f")),o={name:"PagesRegister",components:{PagesBtn:function(){return i.e("chunk-2d0ea0b7").then(i.bind(null,"8fb5"))},PagesHeading:function(){return i.e("chunk-2d0f014c").then(i.bind(null,"9b9f"))}},data:function(){return{agreeText:"I agree the &nbsp;",sections:[{icon:"mdi-chart-timeline-variant",iconColor:"primary",title:"Marketing",text:"We've created the marketing campaign of the website. It was a very interesting collaboration."},{icon:"mdi-code-tags",iconColor:"secondary",title:"Fully Coded in HTML5",text:"We've developed the website with HTML5 and CSS3. The client has access to the code using GitHub."},{icon:"mdi-account-multiple",iconColor:"cyan",title:"Built Audience",text:"There is also a Fully Customizable CMS Admin Dashboard for this product."},{icon:"mdi-account",iconColor:"cyan",title:"Built Audience",text:"There is also a Fully Customizable CMS Admin Dashboard for this product."}],nickname:"",username:"",password:"",confirmPassword:"",checkAgreement:!1}},methods:{register:function(){var t=this;this.nickname?this.username?this.password?this.confirmPassword?this.checkAgreement?this.password!==this.confirmPassword?this.$store.dispatch("openSnackBar",{msg:"The confirm password does not match with the password !!!"}):Object(a["b"])({nickname:this.nickname,username:this.username,password:this.password}).then((function(e){"200"===e.code&&1===e.result&&(t.$router.push({name:"Login"}),t.$store.dispatch("openSnackBar",{msg:"Register success",color:"black",closeBtnColor:"#4CAF50"}))})).catch((function(t){console.error(t)})):this.$store.dispatch("openSnackBar",{msg:"Please check the agreement !!!"}):this.$store.dispatch("openSnackBar",{msg:"Please confirm the password again in the confirm password field !!!",timeout:8e3}):this.$store.dispatch("openSnackBar",{msg:"Please input the password !!!"}):this.$store.dispatch("openSnackBar",{msg:"Please input the username !!!"}):this.$store.dispatch("openSnackBar",{msg:"Please input the nickname !!!"})}}},r=o,c=(i("075a"),i("2877")),l=i("6544"),u=i.n(l),d=i("b0af"),h=i("15fd"),p=i("5530"),m=(i("25f0"),i("6ca7"),i("ec29"),i("9d26")),f=i("c37a"),v=i("fe09"),g=["title"],b=v["a"].extend({name:"v-checkbox",props:{indeterminate:Boolean,indeterminateIcon:{type:String,default:"$checkboxIndeterminate"},offIcon:{type:String,default:"$checkboxOff"},onIcon:{type:String,default:"$checkboxOn"}},data:function(){return{inputIndeterminate:this.indeterminate}},computed:{classes:function(){return Object(p["a"])(Object(p["a"])({},f["a"].options.computed.classes.call(this)),{},{"v-input--selection-controls":!0,"v-input--checkbox":!0,"v-input--indeterminate":this.inputIndeterminate})},computedIcon:function(){return this.inputIndeterminate?this.indeterminateIcon:this.isActive?this.onIcon:this.offIcon},validationState:function(){if(!this.isDisabled||this.inputIndeterminate)return this.hasError&&this.shouldValidate?"error":this.hasSuccess?"success":null!==this.hasColor?this.computedColor:void 0}},watch:{indeterminate:function(t){var e=this;this.$nextTick((function(){return e.inputIndeterminate=t}))},inputIndeterminate:function(t){this.$emit("update:indeterminate",t)},isActive:function(){this.indeterminate&&(this.inputIndeterminate=!1)}},methods:{genCheckbox:function(){var t=this.attrs$,e=(t.title,Object(h["a"])(t,g));return this.$createElement("div",{staticClass:"v-input--selection-controls__input"},[this.$createElement(m["a"],this.setTextColor(this.validationState,{props:{dense:this.dense,dark:this.dark,light:this.light}}),this.computedIcon),this.genInput("checkbox",Object(p["a"])(Object(p["a"])({},e),{},{"aria-checked":this.inputIndeterminate?"mixed":this.isActive.toString()})),this.genRipple(this.setTextColor(this.rippleState))])},genDefaultSlot:function(){return[this.genCheckbox(),this.genLabel()]}}}),k=i("62ad"),C=i("a523"),y=i("132d"),w=i("da13"),x=i("5d23"),V=i("34c3"),S=i("0fd9"),I=i("0789"),P=i("8654"),A=Object(c["a"])(r,n,s,!1,null,"23695630",null);e["default"]=A.exports;u()(A,{VCard:d["a"],VCheckbox:b,VCol:k["a"],VContainer:C["a"],VIcon:y["a"],VListItem:w["a"],VListItemContent:x["a"],VListItemIcon:V["a"],VListItemSubtitle:x["b"],VListItemTitle:x["c"],VRow:S["a"],VSlideYTransition:I["e"],VTextField:P["a"]})},ec29:function(t,e,i){},fe09:function(t,e,i){"use strict";i.d(e,"b",(function(){return r}));i("d3b7"),i("25f0"),i("4de4");var n=i("c37a"),s=i("5311"),a=i("8547"),o=i("58df");function r(t){t.preventDefault()}e["a"]=Object(o["a"])(n["a"],s["a"],a["a"]).extend({name:"selectable",model:{prop:"inputValue",event:"change"},props:{id:String,inputValue:null,falseValue:null,trueValue:null,multiple:{type:Boolean,default:null},label:String},data:function(){return{hasColor:this.inputValue,lazyValue:this.inputValue}},computed:{computedColor:function(){if(this.isActive)return this.color?this.color:this.isDark&&!this.appIsDark?"white":"primary"},isMultiple:function(){return!0===this.multiple||null===this.multiple&&Array.isArray(this.internalValue)},isActive:function(){var t=this,e=this.value,i=this.internalValue;return this.isMultiple?!!Array.isArray(i)&&i.some((function(i){return t.valueComparator(i,e)})):void 0===this.trueValue||void 0===this.falseValue?e?this.valueComparator(e,i):Boolean(i):this.valueComparator(i,this.trueValue)},isDirty:function(){return this.isActive},rippleState:function(){return this.isDisabled||this.validationState?this.validationState:void 0}},watch:{inputValue:function(t){this.lazyValue=t,this.hasColor=t}},methods:{genLabel:function(){var t=n["a"].options.methods.genLabel.call(this);return t?(t.data.on={click:r},t):t},genInput:function(t,e){return this.$createElement("input",{attrs:Object.assign({"aria-checked":this.isActive.toString(),disabled:this.isDisabled,id:this.computedId,role:t,type:t},e),domProps:{value:this.value,checked:this.isActive},on:{blur:this.onBlur,change:this.onChange,focus:this.onFocus,keydown:this.onKeydown,click:r},ref:"input"})},onBlur:function(){this.isFocused=!1},onClick:function(t){this.onChange(),this.$emit("click",t)},onChange:function(){var t=this;if(this.isInteractive){var e=this.value,i=this.internalValue;if(this.isMultiple){Array.isArray(i)||(i=[]);var n=i.length;i=i.filter((function(i){return!t.valueComparator(i,e)})),i.length===n&&i.push(e)}else i=void 0!==this.trueValue&&void 0!==this.falseValue?this.valueComparator(i,this.trueValue)?this.falseValue:this.trueValue:e?this.valueComparator(i,e)?null:e:!i;this.validate(!0,i),this.internalValue=i,this.hasColor=i}},onFocus:function(){this.isFocused=!0},onKeydown:function(t){}}})}}]);
//# sourceMappingURL=chunk-510ceeed.68cf7393.js.map