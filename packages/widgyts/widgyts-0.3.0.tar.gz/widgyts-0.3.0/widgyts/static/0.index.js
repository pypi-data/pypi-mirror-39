(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[0],{

/***/ "./node_modules/@data-exp-lab/yt-tools/yt_tools.js":
/*!*********************************************************!*\
  !*** ./node_modules/@data-exp-lab/yt-tools/yt_tools.js ***!
  \*********************************************************/
/*! exports provided: FixedResolutionBuffer, Colormap, VariableMesh, ColormapCollection, RGBAValue, __wbindgen_throw */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FixedResolutionBuffer", function() { return FixedResolutionBuffer; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Colormap", function() { return Colormap; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VariableMesh", function() { return VariableMesh; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ColormapCollection", function() { return ColormapCollection; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RGBAValue", function() { return RGBAValue; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "__wbindgen_throw", function() { return __wbindgen_throw; });
/* harmony import */ var _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./yt_tools_bg */ "./node_modules/@data-exp-lab/yt-tools/yt_tools_bg.wasm");
/* tslint:disable */


let cachegetUint8Memory = null;
function getUint8Memory() {
    if (cachegetUint8Memory === null || cachegetUint8Memory.buffer !== _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["memory"].buffer) {
        cachegetUint8Memory = new Uint8Array(_yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["memory"].buffer);
    }
    return cachegetUint8Memory;
}

let WASM_VECTOR_LEN = 0;

function passArray8ToWasm(arg) {
    const ptr = _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["__wbindgen_malloc"](arg.length * 1);
    getUint8Memory().set(arg, ptr / 1);
    WASM_VECTOR_LEN = arg.length;
    return ptr;
}

let cachedTextEncoder = new TextEncoder('utf-8');

function passStringToWasm(arg) {

    const buf = cachedTextEncoder.encode(arg);
    const ptr = _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["__wbindgen_malloc"](buf.length);
    getUint8Memory().set(buf, ptr);
    WASM_VECTOR_LEN = buf.length;
    return ptr;
}

let cachegetFloat64Memory = null;
function getFloat64Memory() {
    if (cachegetFloat64Memory === null || cachegetFloat64Memory.buffer !== _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["memory"].buffer) {
        cachegetFloat64Memory = new Float64Array(_yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["memory"].buffer);
    }
    return cachegetFloat64Memory;
}

function passArrayF64ToWasm(arg) {
    const ptr = _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["__wbindgen_malloc"](arg.length * 8);
    getFloat64Memory().set(arg, ptr / 8);
    WASM_VECTOR_LEN = arg.length;
    return ptr;
}

function isLikeNone(x) {
    return x === undefined || x === null;
}

function freeFixedResolutionBuffer(ptr) {

    _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["__wbg_fixedresolutionbuffer_free"](ptr);
}
/**
*/
class FixedResolutionBuffer {

    free() {
        const ptr = this.ptr;
        this.ptr = 0;
        freeFixedResolutionBuffer(ptr);
    }

    /**
    * @param {number} arg0
    * @param {number} arg1
    * @param {number} arg2
    * @param {number} arg3
    * @param {number} arg4
    * @param {number} arg5
    * @returns {}
    */
    constructor(arg0, arg1, arg2, arg3, arg4, arg5) {
        this.ptr = _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["fixedresolutionbuffer_new"](arg0, arg1, arg2, arg3, arg4, arg5);
    }
    /**
    * @param {VariableMesh} arg0
    * @param {Float64Array} arg1
    * @returns {number}
    */
    deposit(arg0, arg1) {
        const ptr1 = passArrayF64ToWasm(arg1);
        const len1 = WASM_VECTOR_LEN;
        try {
            return _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["fixedresolutionbuffer_deposit"](this.ptr, arg0.ptr, ptr1, len1);

        } finally {
            arg1.set(getFloat64Memory().subarray(ptr1 / 8, ptr1 / 8 + len1));
            _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["__wbindgen_free"](ptr1, len1 * 8);

        }

    }
}

function freeColormap(ptr) {

    _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["__wbg_colormap_free"](ptr);
}
/**
*/
class Colormap {

    free() {
        const ptr = this.ptr;
        this.ptr = 0;
        freeColormap(ptr);
    }

    /**
    * @param {Uint8Array} arg0
    * @returns {}
    */
    constructor(arg0) {
        const ptr0 = passArray8ToWasm(arg0);
        const len0 = WASM_VECTOR_LEN;
        this.ptr = _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["colormap_new"](ptr0, len0);
    }
}

function freeVariableMesh(ptr) {

    _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["__wbg_variablemesh_free"](ptr);
}
/**
*/
class VariableMesh {

    free() {
        const ptr = this.ptr;
        this.ptr = 0;
        freeVariableMesh(ptr);
    }

    /**
    * @param {Float64Array} arg0
    * @param {Float64Array} arg1
    * @param {Float64Array} arg2
    * @param {Float64Array} arg3
    * @param {Float64Array} arg4
    * @returns {}
    */
    constructor(arg0, arg1, arg2, arg3, arg4) {
        const ptr0 = passArrayF64ToWasm(arg0);
        const len0 = WASM_VECTOR_LEN;
        const ptr1 = passArrayF64ToWasm(arg1);
        const len1 = WASM_VECTOR_LEN;
        const ptr2 = passArrayF64ToWasm(arg2);
        const len2 = WASM_VECTOR_LEN;
        const ptr3 = passArrayF64ToWasm(arg3);
        const len3 = WASM_VECTOR_LEN;
        const ptr4 = passArrayF64ToWasm(arg4);
        const len4 = WASM_VECTOR_LEN;
        this.ptr = _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["variablemesh_new"](ptr0, len0, ptr1, len1, ptr2, len2, ptr3, len3, ptr4, len4);
    }
}

function freeColormapCollection(ptr) {

    _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["__wbg_colormapcollection_free"](ptr);
}
/**
*/
class ColormapCollection {

    free() {
        const ptr = this.ptr;
        this.ptr = 0;
        freeColormapCollection(ptr);
    }

    /**
    * @returns {}
    */
    constructor() {
        this.ptr = _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["colormapcollection_new"]();
    }
    /**
    * @param {string} arg0
    * @param {Uint8Array} arg1
    * @returns {void}
    */
    add_colormap(arg0, arg1) {
        const ptr0 = passStringToWasm(arg0);
        const len0 = WASM_VECTOR_LEN;
        const ptr1 = passArray8ToWasm(arg1);
        const len1 = WASM_VECTOR_LEN;
        return _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["colormapcollection_add_colormap"](this.ptr, ptr0, len0, ptr1, len1);
    }
    /**
    * @param {string} arg0
    * @param {Float64Array} arg1
    * @param {Uint8Array} arg2
    * @param {number} arg3
    * @param {number} arg4
    * @param {boolean} arg5
    * @returns {void}
    */
    normalize(arg0, arg1, arg2, arg3, arg4, arg5) {
        const ptr0 = passStringToWasm(arg0);
        const len0 = WASM_VECTOR_LEN;
        const ptr1 = passArrayF64ToWasm(arg1);
        const len1 = WASM_VECTOR_LEN;
        const ptr2 = passArray8ToWasm(arg2);
        const len2 = WASM_VECTOR_LEN;
        try {
            return _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["colormapcollection_normalize"](this.ptr, ptr0, len0, ptr1, len1, ptr2, len2, !isLikeNone(arg3), isLikeNone(arg3) ? 0 : arg3, !isLikeNone(arg4), isLikeNone(arg4) ? 0 : arg4, arg5);

        } finally {
            arg2.set(getUint8Memory().subarray(ptr2 / 1, ptr2 / 1 + len2));
            _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["__wbindgen_free"](ptr2, len2 * 1);

        }

    }
}

function freeRGBAValue(ptr) {

    _yt_tools_bg__WEBPACK_IMPORTED_MODULE_0__["__wbg_rgbavalue_free"](ptr);
}
/**
*/
class RGBAValue {

    free() {
        const ptr = this.ptr;
        this.ptr = 0;
        freeRGBAValue(ptr);
    }

}

let cachedTextDecoder = new TextDecoder('utf-8');

function getStringFromWasm(ptr, len) {
    return cachedTextDecoder.decode(getUint8Memory().subarray(ptr, ptr + len));
}

function __wbindgen_throw(ptr, len) {
    throw new Error(getStringFromWasm(ptr, len));
}



/***/ }),

/***/ "./node_modules/@data-exp-lab/yt-tools/yt_tools_bg.wasm":
/*!**************************************************************!*\
  !*** ./node_modules/@data-exp-lab/yt-tools/yt_tools_bg.wasm ***!
  \**************************************************************/
/*! exports provided: memory, __wbg_rgbavalue_free, __wbg_colormap_free, __wbg_colormapcollection_free, colormap_new, colormapcollection_new, colormapcollection_add_colormap, colormapcollection_normalize, __wbg_variablemesh_free, variablemesh_new, __wbg_fixedresolutionbuffer_free, fixedresolutionbuffer_new, fixedresolutionbuffer_deposit, __wbindgen_malloc, __wbindgen_free */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
// Instantiate WebAssembly module
var wasmExports = __webpack_require__.w[module.i];
__webpack_require__.r(exports);
// export exports from WebAssembly module
for(var name in wasmExports) if(name != "__webpack_init__") exports[name] = wasmExports[name];
// exec imports from WebAssembly module (for esm order)
/* harmony import */ var m0 = __webpack_require__(/*! ./yt_tools */ "./node_modules/@data-exp-lab/yt-tools/yt_tools.js");


// exec wasm module
wasmExports["__webpack_init__"]()

/***/ })

}]);
//# sourceMappingURL=0.index.js.map