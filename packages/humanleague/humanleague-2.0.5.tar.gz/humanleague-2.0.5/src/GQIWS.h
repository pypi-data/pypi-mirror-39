

#pragma once

#include "QIWS.h"

struct ConstrainG
{
  enum Status { SUCCESS = 0, ITERLIMIT = 1, STUCK = 2 };
};


// 2-Dimensional generalised quasirandom integer without-replacement sampling
// TODO rename
//template<size_t D>
class GQIWS : public QIWS
{
public:

  GQIWS(const std::vector<marginal_t>& marginals, const NDArray<double>& exoProbs);

  ~GQIWS() { }

  GQIWS(const GQIWS&) = delete;

  bool solve();

  // allow constraining of precomputed populations
  //static Constrain::Status constrain(NDArray<2, uint32_t>& pop, const NDArray<2, bool>& allowedStates, const size_t iterLimit);

private:
  // no copy semantics so just store a ref (possibly dangerous)
  // TODO use move semantics
  const NDArray<double>& m_exoprobs;

};






