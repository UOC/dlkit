/**
 * @fileoverview
 * @enhanceable
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 */
// GENERATED CODE -- DO NOT EDIT!

var jspb = require('google-protobuf');
var goog = jspb;
var global = Function('return this')();

var dlkit_primordium_type_primitives_pb = require('../../../dlkit/primordium/type/primitives_pb.js');
goog.exportSymbol('proto.dlkit.primordium.locale.primitives.DisplayText', null, global);

/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.dlkit.primordium.locale.primitives.DisplayText = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.dlkit.primordium.locale.primitives.DisplayText, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  proto.dlkit.primordium.locale.primitives.DisplayText.displayName = 'proto.dlkit.primordium.locale.primitives.DisplayText';
}


if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto suitable for use in Soy templates.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     com.google.apps.jspb.JsClassTemplate.JS_RESERVED_WORDS.
 * @param {boolean=} opt_includeInstance Whether to include the JSPB instance
 *     for transitional soy proto support: http://goto/soy-param-migration
 * @return {!Object}
 */
proto.dlkit.primordium.locale.primitives.DisplayText.prototype.toObject = function(opt_includeInstance) {
  return proto.dlkit.primordium.locale.primitives.DisplayText.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Whether to include the JSPB
 *     instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.dlkit.primordium.locale.primitives.DisplayText} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.dlkit.primordium.locale.primitives.DisplayText.toObject = function(includeInstance, msg) {
  var f, obj = {
    text: jspb.Message.getFieldWithDefault(msg, 1, ""),
    formatTypeId: (f = msg.getFormatTypeId()) && dlkit_primordium_type_primitives_pb.Type.toObject(includeInstance, f),
    languageTypeId: (f = msg.getLanguageTypeId()) && dlkit_primordium_type_primitives_pb.Type.toObject(includeInstance, f),
    scriptTypeId: (f = msg.getScriptTypeId()) && dlkit_primordium_type_primitives_pb.Type.toObject(includeInstance, f)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.dlkit.primordium.locale.primitives.DisplayText}
 */
proto.dlkit.primordium.locale.primitives.DisplayText.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.dlkit.primordium.locale.primitives.DisplayText;
  return proto.dlkit.primordium.locale.primitives.DisplayText.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.dlkit.primordium.locale.primitives.DisplayText} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.dlkit.primordium.locale.primitives.DisplayText}
 */
proto.dlkit.primordium.locale.primitives.DisplayText.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setText(value);
      break;
    case 2:
      var value = new dlkit_primordium_type_primitives_pb.Type;
      reader.readMessage(value,dlkit_primordium_type_primitives_pb.Type.deserializeBinaryFromReader);
      msg.setFormatTypeId(value);
      break;
    case 3:
      var value = new dlkit_primordium_type_primitives_pb.Type;
      reader.readMessage(value,dlkit_primordium_type_primitives_pb.Type.deserializeBinaryFromReader);
      msg.setLanguageTypeId(value);
      break;
    case 4:
      var value = new dlkit_primordium_type_primitives_pb.Type;
      reader.readMessage(value,dlkit_primordium_type_primitives_pb.Type.deserializeBinaryFromReader);
      msg.setScriptTypeId(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.dlkit.primordium.locale.primitives.DisplayText.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.dlkit.primordium.locale.primitives.DisplayText.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.dlkit.primordium.locale.primitives.DisplayText} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.dlkit.primordium.locale.primitives.DisplayText.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getText();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getFormatTypeId();
  if (f != null) {
    writer.writeMessage(
      2,
      f,
      dlkit_primordium_type_primitives_pb.Type.serializeBinaryToWriter
    );
  }
  f = message.getLanguageTypeId();
  if (f != null) {
    writer.writeMessage(
      3,
      f,
      dlkit_primordium_type_primitives_pb.Type.serializeBinaryToWriter
    );
  }
  f = message.getScriptTypeId();
  if (f != null) {
    writer.writeMessage(
      4,
      f,
      dlkit_primordium_type_primitives_pb.Type.serializeBinaryToWriter
    );
  }
};


/**
 * optional string text = 1;
 * @return {string}
 */
proto.dlkit.primordium.locale.primitives.DisplayText.prototype.getText = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/** @param {string} value */
proto.dlkit.primordium.locale.primitives.DisplayText.prototype.setText = function(value) {
  jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional dlkit.primordium.type.primitives.Type format_type_id = 2;
 * @return {?proto.dlkit.primordium.type.primitives.Type}
 */
proto.dlkit.primordium.locale.primitives.DisplayText.prototype.getFormatTypeId = function() {
  return /** @type{?proto.dlkit.primordium.type.primitives.Type} */ (
    jspb.Message.getWrapperField(this, dlkit_primordium_type_primitives_pb.Type, 2));
};


/** @param {?proto.dlkit.primordium.type.primitives.Type|undefined} value */
proto.dlkit.primordium.locale.primitives.DisplayText.prototype.setFormatTypeId = function(value) {
  jspb.Message.setWrapperField(this, 2, value);
};


proto.dlkit.primordium.locale.primitives.DisplayText.prototype.clearFormatTypeId = function() {
  this.setFormatTypeId(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.dlkit.primordium.locale.primitives.DisplayText.prototype.hasFormatTypeId = function() {
  return jspb.Message.getField(this, 2) != null;
};


/**
 * optional dlkit.primordium.type.primitives.Type language_type_id = 3;
 * @return {?proto.dlkit.primordium.type.primitives.Type}
 */
proto.dlkit.primordium.locale.primitives.DisplayText.prototype.getLanguageTypeId = function() {
  return /** @type{?proto.dlkit.primordium.type.primitives.Type} */ (
    jspb.Message.getWrapperField(this, dlkit_primordium_type_primitives_pb.Type, 3));
};


/** @param {?proto.dlkit.primordium.type.primitives.Type|undefined} value */
proto.dlkit.primordium.locale.primitives.DisplayText.prototype.setLanguageTypeId = function(value) {
  jspb.Message.setWrapperField(this, 3, value);
};


proto.dlkit.primordium.locale.primitives.DisplayText.prototype.clearLanguageTypeId = function() {
  this.setLanguageTypeId(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.dlkit.primordium.locale.primitives.DisplayText.prototype.hasLanguageTypeId = function() {
  return jspb.Message.getField(this, 3) != null;
};


/**
 * optional dlkit.primordium.type.primitives.Type script_type_id = 4;
 * @return {?proto.dlkit.primordium.type.primitives.Type}
 */
proto.dlkit.primordium.locale.primitives.DisplayText.prototype.getScriptTypeId = function() {
  return /** @type{?proto.dlkit.primordium.type.primitives.Type} */ (
    jspb.Message.getWrapperField(this, dlkit_primordium_type_primitives_pb.Type, 4));
};


/** @param {?proto.dlkit.primordium.type.primitives.Type|undefined} value */
proto.dlkit.primordium.locale.primitives.DisplayText.prototype.setScriptTypeId = function(value) {
  jspb.Message.setWrapperField(this, 4, value);
};


proto.dlkit.primordium.locale.primitives.DisplayText.prototype.clearScriptTypeId = function() {
  this.setScriptTypeId(undefined);
};


/**
 * Returns whether this field is set.
 * @return {!boolean}
 */
proto.dlkit.primordium.locale.primitives.DisplayText.prototype.hasScriptTypeId = function() {
  return jspb.Message.getField(this, 4) != null;
};


goog.object.extend(exports, proto.dlkit.primordium.locale.primitives);
