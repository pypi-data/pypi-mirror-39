/** Opaque data structure that stores a base point
 *
 *  The exact representation of data inside is implementation defined and not
 *  guaranteed to be portable between different platforms or versions. It is
 *  however guaranteed to be 33 bytes in size, and can be safely copied/moved.
 *  If you need to convert to a format suitable for storage or transmission, use
 *  the secp256k1_generator_serialize_*.
 *
 *  Furthermore, it is guaranteed to identical points will have identical
 *  representation, so they can be memcmp'ed.
 */
typedef struct {
    unsigned char data[64];
} secp256k1_generator;

extern const secp256k1_generator secp256k1_generator_const_g;
extern const secp256k1_generator secp256k1_generator_const_h;

/** Parse a 33-byte generator byte sequence into a generator object.
 *
 *  Returns: 1 if input contains a valid generator.
 *  Args: ctx:      a secp256k1 context object.
 *  Out:  commit:   pointer to the output generator object
 *  In:   input:    pointer to a 33-byte serialized generator
 */
int secp256k1_generator_parse(
    const secp256k1_context* ctx,
    secp256k1_generator* commit,
    const unsigned char *input
);

/** Serialize a 33-byte generator into a serialized byte sequence.
 *
 *  Returns: 1 always.
 *  Args:   ctx:        a secp256k1 context object.
 *  Out:    output:     a pointer to a 33-byte byte array
 *  In:     commit:     a pointer to a generator
 */
int secp256k1_generator_serialize(
    const secp256k1_context* ctx,
    unsigned char *output,
    const secp256k1_generator* commit
);

/** Generate a generator for the curve.
 *
 *  Returns: 0 in the highly unlikely case the seed is not acceptable,
 *           1 otherwise.
 *  Args: ctx:     a secp256k1 context object
 *  Out:  gen:     a generator object
 *  In:   seed32:  a 32-byte seed
 *
 *  If succesful, a valid generator will be placed in gen. The produced
 *  generators are distributed uniformly over the curve, and will not have a
 *  known dicrete logarithm with respect to any other generator produced,
 *  or to the base generator G.
 */
int secp256k1_generator_generate(
    const secp256k1_context* ctx,
    secp256k1_generator* gen,
    const unsigned char *seed32
);

/** Generate a blinded generator for the curve.
 *
 *  Returns: 0 in the highly unlikely case the seed is not acceptable or when
 *           blind is out of range. 1 otherwise.
 *  Args: ctx:     a secp256k1 context object, initialized for signing
 *  Out:  gen:     a generator object
 *  In:   seed32:  a 32-byte seed
 *        blind32: a 32-byte secret value to blind the generator with.
 *
 *  The result is equivalent to first calling secp256k1_generator_generate,
 *  converting the result to a public key, calling secp256k1_ec_pubkey_tweak_add,
 *  and then converting back to generator form.
 */
int secp256k1_generator_generate_blinded(
    const secp256k1_context* ctx,
    secp256k1_generator* gen,
    const unsigned char *key32,
    const unsigned char *blind32
);



typedef struct {
    unsigned char data[64];
} secp256k1_pedersen_commitment;


/** Parse a 33-byte commitment into a commitment object.
 *
 *  Returns: 1 if input contains a valid commitment.
 *  Args: ctx:      a secp256k1 context object.
 *  Out:  commit:   pointer to the output commitment object
 *  In:   input:    pointer to a 33-byte serialized commitment key
 */
int secp256k1_pedersen_commitment_parse(
    const secp256k1_context* ctx,
    secp256k1_pedersen_commitment* commit,
    const unsigned char *input
);

/** Serialize a commitment object into a serialized byte sequence.
 *
 *  Returns: 1 always.
 *  Args:   ctx:        a secp256k1 context object.
 *  Out:    output:     a pointer to a 33-byte byte array
 *  In:     commit:     a pointer to a secp256k1_pedersen_commitment containing an
 *                      initialized commitment
 */
int secp256k1_pedersen_commitment_serialize(
    const secp256k1_context* ctx,
    unsigned char *output,
    const secp256k1_pedersen_commitment* commit
);


/** Generate a pedersen commitment.
 *  Returns 1: Commitment successfully created.
 *          0: Error. The blinding factor is larger than the group order
 *             (probability for random 32 byte number < 2^-127) or results in the
 *             point at infinity. Retry with a different factor.
 *  In:     ctx:        pointer to a context object, initialized for signing and Pedersen commitment (cannot be NULL)
 *          blind:      pointer to a 32-byte blinding factor (cannot be NULL)
 *          value:      unsigned 64-bit integer value to commit to.
 *          gen:        additional generator 'h'
 *  Out:    commit:     pointer to the commitment (cannot be NULL)
 *
 *  Blinding factors can be generated and verified in the same way as secp256k1 private keys for ECDSA.
 */
int secp256k1_pedersen_commit(
  const secp256k1_context* ctx,
  secp256k1_pedersen_commitment *commit,
  const unsigned char *blind,
  uint64_t value,
  const secp256k1_generator *value_gen,
  const secp256k1_generator *blind_gen
);

/** Computes the sum of multiple positive and negative blinding factors.
 *  Returns 1: Sum successfully computed.
 *          0: Error. A blinding factor is larger than the group order
 *             (probability for random 32 byte number < 2^-127). Retry with
 *             different factors.
 *  In:     ctx:        pointer to a context object (cannot be NULL)
 *          blinds:     pointer to pointers to 32-byte character arrays for blinding factors. (cannot be NULL)
 *          n:          number of factors pointed to by blinds.
 *          npositive:       how many of the initial factors should be treated with a positive sign.
 *  Out:    blind_out:  pointer to a 32-byte array for the sum (cannot be NULL)
 */
int secp256k1_pedersen_blind_sum(
  const secp256k1_context* ctx,
  unsigned char *blind_out,
  const unsigned char * const *blinds,
  size_t n,
  size_t npositive
);

/** Verify a tally of pedersen commitments
 * Returns 1: commitments successfully sum to zero.
 *         0: Commitments do not sum to zero or other error.
 * In:     ctx:        pointer to a context object (cannot be NULL)
 *         commits:    pointer to array of pointers to the commitments. (cannot be NULL if pcnt is non-zero)
 *         pcnt:       number of commitments pointed to by commits.
 *         ncommits:   pointer to array of pointers to the negative commitments. (cannot be NULL if ncnt is non-zero)
 *         ncnt:       number of commitments pointed to by ncommits.
 *
 * This computes sum(commit[0..pcnt)) - sum(ncommit[0..ncnt)) == 0.
 *
 * A pedersen commitment is xG + vA where G and A are generators for the secp256k1 group and x is a blinding factor,
 * while v is the committed value. For a collection of commitments to sum to zero, for each distinct generator
 * A all blinding factors and all values must sum to zero.
 *
 */
int secp256k1_pedersen_verify_tally(
  const secp256k1_context* ctx,
  const secp256k1_pedersen_commitment * const* commits,
  size_t pcnt,
  const secp256k1_pedersen_commitment * const* ncommits,
  size_t ncnt
);

/** Sets the final Pedersen blinding factor correctly when the generators themselves
 *  have blinding factors.
 *
 * Consider a generator of the form A' = A + rG, where A is the "real" generator
 * but A' is the generator provided to verifiers. Then a Pedersen commitment
 * P = vA' + r'G really has the form vA + (vr + r')G. To get all these (vr + r')
 * to sum to zero for multiple commitments, we take three arrays consisting of
 * the `v`s, `r`s, and `r'`s, respectively called `value`s, `generator_blind`s
 * and `blinding_factor`s, and sum them.
 *
 * The function then subtracts the sum of all (vr + r') from the last element
 * of the `blinding_factor` array, setting the total sum to zero.
 *
 * Returns 1: Blinding factor successfully computed.
 *         0: Error. A blinding_factor or generator_blind are larger than the group
 *            order (probability for random 32 byte number < 2^-127). Retry with
 *            different values.
 *
 * In:                 ctx: pointer to a context object
 *                   value: array of asset values, `v` in the above paragraph.
 *                          May not be NULL unless `n_total` is 0.
 *         generator_blind: array of asset blinding factors, `r` in the above paragraph
 *                          May not be NULL unless `n_total` is 0.
 *                 n_total: Total size of the above arrays
 *                n_inputs: How many of the initial array elements represent commitments that
 *                          will be negated in the final sum
 * In/Out: blinding_factor: array of commitment blinding factors, `r'` in the above paragraph
 *                          May not be NULL unless `n_total` is 0.
 *                          the last value will be modified to get the total sum to zero.
 */
int secp256k1_pedersen_blind_generator_blind_sum(
  const secp256k1_context* ctx,
  const uint64_t *value,
  const unsigned char* const* generator_blind,
  unsigned char* const* blinding_factor,
  size_t n_total,
  size_t n_inputs
);



/** Verify a proof that a committed value is within a range.
 * Returns 1: Value is within the range [0..2^64), the specifically proven range is in the min/max value outputs.
 *         0: Proof failed or other error.
 * In:   ctx: pointer to a context object, initialized for range-proof and commitment (cannot be NULL)
 *       commit: the commitment being proved. (cannot be NULL)
 *       proof: pointer to character array with the proof. (cannot be NULL)
 *       plen: length of proof in bytes.
 *       extra_commit: additional data covered in rangeproof signature
 *       extra_commit_len: length of extra_commit byte array (0 if NULL)
 *       gen: additional generator 'h'
 * Out:  min_value: pointer to a unsigned int64 which will be updated with the minimum value that commit could have. (cannot be NULL)
 *       max_value: pointer to a unsigned int64 which will be updated with the maximum value that commit could have. (cannot be NULL)
 */
int secp256k1_rangeproof_verify(
  const secp256k1_context* ctx,
  uint64_t *min_value,
  uint64_t *max_value,
  const secp256k1_pedersen_commitment *commit,
  const unsigned char *proof,
  size_t plen,
  const unsigned char *extra_commit,
  size_t extra_commit_len,
  const secp256k1_generator* gen
);

/** Verify a range proof proof and rewind the proof to recover information sent by its author.
 *  Returns 1: Value is within the range [0..2^64), the specifically proven range is in the min/max value outputs, and the value and blinding were recovered.
 *          0: Proof failed, rewind failed, or other error.
 *  In:   ctx: pointer to a context object, initialized for range-proof and Pedersen commitment (cannot be NULL)
 *        commit: the commitment being proved. (cannot be NULL)
 *        proof: pointer to character array with the proof. (cannot be NULL)
 *        plen: length of proof in bytes.
 *        nonce: 32-byte secret nonce used by the prover (cannot be NULL)
 *        extra_commit: additional data covered in rangeproof signature
 *        extra_commit_len: length of extra_commit byte array (0 if NULL)
 *        gen: additional generator 'h'
 *  In/Out: blind_out: storage for the 32-byte blinding factor used for the commitment
 *        value_out: pointer to an unsigned int64 which has the exact value of the commitment.
 *        message_out: pointer to a 4096 byte character array to receive message data from the proof author.
 *        outlen:  length of message data written to message_out.
 *        min_value: pointer to an unsigned int64 which will be updated with the minimum value that commit could have. (cannot be NULL)
 *        max_value: pointer to an unsigned int64 which will be updated with the maximum value that commit could have. (cannot be NULL)
 */
int secp256k1_rangeproof_rewind(
  const secp256k1_context* ctx,
  unsigned char *blind_out,
  uint64_t *value_out,
  unsigned char *message_out,
  size_t *outlen,
  const unsigned char *nonce,
  uint64_t *min_value,
  uint64_t *max_value,
  const secp256k1_pedersen_commitment *commit,
  const unsigned char *proof,
  size_t plen,
  const unsigned char *extra_commit,
  size_t extra_commit_len,
  const secp256k1_generator *gen
);

/** Author a proof that a committed value is within a range.
 *  Returns 1: Proof successfully created.
 *          0: Error
 *  In:     ctx:    pointer to a context object, initialized for range-proof, signing, and Pedersen commitment (cannot be NULL)
 *          proof:  pointer to array to receive the proof, can be up to 5134 bytes. (cannot be NULL)
 *          min_value: constructs a proof where the verifer can tell the minimum value is at least the specified amount.
 *          commit: the commitment being proved.
 *          blind:  32-byte blinding factor used by commit.
 *          nonce:  32-byte secret nonce used to initialize the proof (value can be reverse-engineered out of the proof if this secret is known.)
 *          exp:    Base-10 exponent. Digits below above will be made public, but the proof will be made smaller. Allowed range is -1 to 18.
 *                  (-1 is a special case that makes the value public. 0 is the most private.)
 *          min_bits: Number of bits of the value to keep private. (0 = auto/minimal, - 64).
 *          value:  Actual value of the commitment.
 *          message: pointer to a byte array of data to be embedded in the rangeproof that can be recovered by rewinding the proof
 *          msg_len: size of the message to be embedded in the rangeproof
 *          extra_commit: additional data to be covered in rangeproof signature
 *          extra_commit_len: length of extra_commit byte array (0 if NULL)
 *          gen: additional generator 'h'
 *  In/out: plen:   point to an integer with the size of the proof buffer and the size of the constructed proof.
 *
 *  If min_value or exp is non-zero then the value must be on the range [0, 2^63) to prevent the proof range from spanning past 2^64.
 *
 *  If exp is -1 the value is revealed by the proof (e.g. it proves that the proof is a blinding of a specific value, without revealing the blinding key.)
 *
 *  This can randomly fail with probability around one in 2^100. If this happens, buy a lottery ticket and retry with a different nonce or blinding.
 *
 */
int secp256k1_rangeproof_sign(
  const secp256k1_context* ctx,
  unsigned char *proof,
  size_t *plen,
  uint64_t min_value,
  const secp256k1_pedersen_commitment *commit,
  const unsigned char *blind,
  const unsigned char *nonce,
  int exp,
  int min_bits,
  uint64_t value,
  const unsigned char *message,
  size_t msg_len,
  const unsigned char *extra_commit,
  size_t extra_commit_len,
  const secp256k1_generator *gen
);

/** Extract some basic information from a range-proof.
 *  Returns 1: Information successfully extracted.
 *          0: Decode failed.
 *  In:   ctx: pointer to a context object
 *        proof: pointer to character array with the proof.
 *        plen: length of proof in bytes.
 *  Out:  exp: Exponent used in the proof (-1 means the value isn't private).
 *        mantissa: Number of bits covered by the proof.
 *        min_value: pointer to an unsigned int64 which will be updated with the minimum value that commit could have. (cannot be NULL)
 *        max_value: pointer to an unsigned int64 which will be updated with the maximum value that commit could have. (cannot be NULL)
 */
int secp256k1_rangeproof_info(
  const secp256k1_context* ctx,
  int *exp,
  int *mantissa,
  uint64_t *min_value,
  uint64_t *max_value,
  const unsigned char *proof,
  size_t plen
);


